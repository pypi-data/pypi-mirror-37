from typing import Dict, Any, List, Optional, Tuple
from abc import ABCMeta
from datetime import datetime
import logging

from .fields import Field, compute_field
from .fields.base import ComputeField
from .ast import QueryAst, QueryTable
from .indexes import IndexPolicy, IndexPolicySetting, IndexPolicySettings
from .register import orm_register
from .utils import merge_dicts

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['Model', 'ModelMetaclass', 'ModifyDisallowException']

MODEL_FIELDS_CONTROL = {
    '_aggregate_dict': ['_fields', '_field_marks'],
    '_inherit_field': ['_table'],
}

_log = logging.getLogger(__name__)


class ModifyDisallowException(Exception):
    """
    Exception that raises when you try change `Model` class field that blocked for changes
    """
    pass


class ModelMetaclass(ABCMeta):

    @classmethod
    def _aggregate_dict(mcs, bases, namespace, field):
        actual_field = {}
        for base_class in bases:
            if hasattr(base_class, field):
                actual_field.update(getattr(base_class, field))
        if namespace.get(field, None):
            actual_field.update(namespace.get(field))
        namespace[field] = actual_field

    @classmethod
    def _inherit_field(mcs, bases, namespace: Dict, field: str):
        current_field_exists = field in namespace
        if not current_field_exists:
            for base_class in bases:
                if hasattr(base_class, field):
                    namespace[field] = getattr(base_class, field)
                    break

    @classmethod
    def _deep_merge_dict(mcs, bases, namespace: Dict, field: str):
        actual_field: Dict = {}
        for base_class in bases:
            if hasattr(base_class, field):
                merge_dicts(getattr(base_class, field), actual_field)
        if namespace.get(field, None):
            merge_dicts(namespace.get(field), actual_field)
        namespace[field] = actual_field

    @classmethod
    def _fetch_fields(mcs, namespace):
        fields = namespace.get('_fields', None) or {}
        field_marks = {}
        type_annotations = namespace.get('__annotations__', {})
        for attr_name in type_annotations:
            attr = namespace.get(attr_name, None)
            # Skip hided fields that not Field really
            if attr_name.startswith('_') and not isinstance(attr, Field):
                continue
            if not isinstance(attr, Field):
                attr_field = Field(default=attr)
            else:
                attr_field = attr
            attr_field.param_type = type_annotations[attr_name]
            namespace[attr_name] = attr_field
            fields[attr_name] = attr_field
            if attr_field.field_marks:
                for field_mark in attr_field.field_marks:
                    field_marks[field_mark] = attr_name
        namespace['_fields'] = fields
        namespace['_field_marks'] = field_marks

    @classmethod
    def _fetch_compute_fields(mcs, namespace):
        for attr_name in list(namespace.keys()):
            attr = namespace[attr_name]
            if callable(attr) and hasattr(attr, '_anji_compute_field'):
                field = ComputeField(attr, **attr._anji_compute_field_kwargs)
                namespace[attr_name] = field
                namespace['_fields'][attr_name] = field

    def __new__(mcs, name, bases, namespace, **kwargs):

        # Process fields

        mcs._fetch_fields(namespace)
        mcs._fetch_compute_fields(namespace)

        # Execute control actions

        for key, value in MODEL_FIELDS_CONTROL.items():
            if hasattr(mcs, key):
                for field in value:
                    getattr(mcs, key)(bases, namespace, field)

        if '__slots__' not in namespace:
            namespace['__slots__'] = ()

        # Process with register
        result = super().__new__(mcs, name, bases, namespace, **kwargs)

        if namespace.get('_table'):
            orm_register.add_table(namespace.get('_table'), result)

        return result


class Model(metaclass=ModelMetaclass):  # pylint: disable=too-many-public-methods
    """
    Base class with core logic for rethinkdb usage.
    For usage you must define _table and _fields section.
    All object fields, that defined in _fields will be processed in send() and load() methods
    """

    _table = ''
    _fields: Dict[str, Field] = {}
    _field_marks: Dict[str, Field] = {}
    _primary_keys: List[str] = []
    _index_policy: IndexPolicy = IndexPolicy.single

    _index_policy_settings: IndexPolicySettings = {
        IndexPolicySetting.only_single_index: ('_schema_version',)
    }

    orm_last_write_timestamp: Optional[datetime]
    _schema_version: str = Field(internal=True, default='v0.4', secondary_index=True)  # type: ignore
    id: Optional[str]

    __slots__ = ('_meta', '_values')

    def __init__(self, **kwargs) -> None:
        """
        Complex init method for rethinkdb method.
        Next tasks will be executed:
        1. Create all fields, that defined in _fields, for object
        3. Set base fields, like connection link.
            Additionally can set id field in some cases (for example in fetch method)
        4. Create table field, to be used in queries
        """
        self._values: Dict[str, Any] = dict()
        self._meta: Dict = dict()
        # init from deafult
        for field_name, field in self._fields.items():
            if field.is_setable:
                if field_name in kwargs:
                    setattr(self, field_name, kwargs[field_name])
                else:
                    setattr(self, field_name, field.get_default())

    @compute_field(internal=True, stored=True)
    def _python_info(self) -> Dict[str, str]:
        return {
            'module_name': self.__class__.__module__,
            'class_name': self.__class__.__name__
        }

    def to_dict(self, full_dict: bool = False) -> Dict[str, Any]:
        """
        Utility method to generate dict from object.
        Used to send information to rethinkdb.

        :param full_dict: Build full data dict with non-stored fields
        """
        base_dict = {}
        for field_name, field_item in self._fields.items():
            if not full_dict and isinstance(field_item, ComputeField) and not field_item.stored:
                _log.debug('Skip field %s as not stored field', field_name)
                continue
            base_dict[field_name] = field_item.real_value(self)
        # Ignore id when empty
        if not base_dict['id']:
            del base_dict['id']
        return base_dict

    def _apply_update_dict(self, update_dict: Dict[str, Any]) -> None:
        for field_key, update_value in update_dict.items():
            if field_key in self._fields:
                setattr(self, field_key, update_value)

    def from_dict(self, data_dict: Dict[str, Any], meta: Dict = None) -> None:
        """
        Load model record from dict

        :param data_dict: dict with data from RethinkDB
        """
        for field_name, field_item in self._fields.items():
            if field_name in data_dict and field_item.is_setable:
                setattr(self, field_name, data_dict[field_name])
        if meta:
            self._meta = meta

    @classmethod
    def build_index_list(cls) -> List[Tuple[str, List[str]]]:
        return cls._index_policy.value.build_index_list(cls)  # pylint: disable=no-member

    def load(self, data_dict=None, meta=None) -> None:
        if not data_dict:
            data_dict, meta = orm_register.shared.executor.load_model(self)
        self.from_dict(data_dict, meta=meta)

    async def async_load(self, data_dict=None, meta=None) -> None:
        if not data_dict:
            data_dict, meta = await orm_register.shared.executor.load_model(self)
        self.from_dict(data_dict, meta=meta)

    def send(self) -> None:
        orm_register.shared.executor.send_model(self)

    async def async_send(self) -> None:
        await orm_register.shared.executor.send_model(self)

    def delete(self) -> None:
        orm_register.shared.executor.delete_model(self)

    async def async_delete(self) -> None:
        await orm_register.shared.executor.delete_model(self)

    @classmethod
    def get(cls, id_) -> Optional['Model']:
        return orm_register.shared.executor.get_model(cls, id_)

    @classmethod
    async def async_get(cls, id_) -> Optional['Model']:
        return await orm_register.shared.executor.get_model(cls, id_)

    @classmethod
    def all(cls) -> QueryAst:
        return QueryTable(cls._table, model_ref=cls)

    def update(self, update_dict: Dict[str, Any]) -> None:
        self._apply_update_dict(update_dict)
        self.send()

    async def async_update(self, update_dict: Dict[str, Any]) -> None:
        self._apply_update_dict(update_dict)
        await self.async_send()

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        for field_name, field in self._fields.items():
            if field.internal:
                continue
            if getattr(self, field_name) != getattr(other, field_name):
                return False
        return True

    def __repr__(self) -> str:
        values = ", ".join(
            f"{key}={getattr(self, key)}" for key, field in self._fields.items()
            if not field.internal
        )
        return f'{self.__class__.__name__}[{values}]'
