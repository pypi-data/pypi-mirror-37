import asyncio
from typing import Type, Any, List, Union, Dict, Optional, Callable, TYPE_CHECKING
import inspect
import logging
import functools

from ..ast.rows import QueryRow, BooleanQueryRow, DictQueryRow
from ..register import orm_register
from ..utils import prettify_value

if TYPE_CHECKING:
    from ..model import Model  # pylint: disable=unused-import

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = [
    'Field', 'compute_field'
]

_log = logging.getLogger(__name__)


def _type_check(value: Any, target_type: Type) -> bool:
    if hasattr(target_type, '__args__'):
        if target_type.__origin__ is Union:
            return any(_type_check(value, x) for x in target_type.__args__)
        checking_type = target_type if not hasattr(target_type, '_gorg') else target_type._gorg
        base_result = isinstance(value, checking_type)
        # TODO: process advanced type checking!
        return base_result
    return isinstance(value, target_type)


def _none_factory():
    return None


ROW_TYPE_MAPPING: Dict[Type, Type[QueryRow]] = {
    bool: BooleanQueryRow,
    Dict: DictQueryRow
}


class Field:  # pylint:disable=too-many-instance-attributes

    """
    Base ORM field class. Used to describe base logic and provide unified type check
    """

    _anji_orm_field: bool = True

    __slots__ = (
        'default', 'default_factory', 'description',
        'internal', 'field_marks', 'secondary_index',
        # Service or calculate fields
        'name', '_param_type', '_query_row'
    )

    def __init__(
            self, default: Any = None, default_factory: Optional[Callable] = None,
            description: str = '', internal: bool = False, field_marks: Optional[List[str]] = None,
            secondary_index: bool = False) -> None:
        """
        Init function for ORM fields. Provide parameter checks with assertion

        :param default: Field default value, should be strict value. Default value is None.
        :param default_factory: Function without params, that return required default
        :param description: Field description, mostly used for automatic generated commands. Default value is empty string.
        :param internal: If true, this field used only in internal bot logic. Default value is False.
        :param field_marks: Additional field marks, to use in internal logic. Default value is None.
        :param bool secondary_index: If true, ORM will build secondary_index on this field. Default value is False.
        """
        # Setup fields
        if not ((default is None) or (default_factory is None)):
            raise ValueError("Cannot use field with default and default_factory, please, choose one")
        self.default = default
        self.default_factory = default_factory or _none_factory
        self.description = description
        self.internal = internal
        self.field_marks = field_marks
        self.secondary_index = secondary_index
        # Name will be set by Model Metaclass, by :code:`__set_name__`
        # when field list be fetched
        self.name: str
        self._query_row: QueryRow
        self._param_type: Type

    @property
    def param_type(self) -> Type:
        return self._param_type

    @param_type.setter
    def param_type(self, value: Type) -> None:
        self._param_type = value

    def __set_name__(self, owner, name) -> None:
        self.name = name
        target_type = self.param_type
        # Special check for Optinal case
        if hasattr(self.param_type, '__origin__') and self.param_type.__origin__ is Union:
            none_type = type(None)
            real_params = [x for x in self.param_type.__args__ if x is not none_type]  # type: ignore
            if len(real_params) == 1:
                target_type = real_params[0]
        self._query_row = ROW_TYPE_MAPPING.get(target_type, QueryRow)(
            self.name, secondary_index=self.secondary_index, model_ref=owner
        )

    def get_default(self):
        return self.default or self.default_factory()

    def real_value(self, model_record):
        """
        Based on __get__ method, but can be used to split overrided __get__ method
        like for LinkField from real infomration
        """
        return prettify_value(self.__get__(model_record, None))

    def __get__(self, instance, instance_type):
        if instance is None:
            return self._query_row
        return instance._values[self.name]

    def __set__(self, instance, value) -> None:
        if not _type_check(value, self.param_type):
            raise ValueError(f'Field {self.name} value should have {str(self.param_type)} type instead of {value}')
        instance._values[self.name] = orm_register.backend_adapter.ensure_representation_compatibility(value)

    @property
    def is_setable(self) -> bool:
        return True

    def can_be(self, target_type: Type) -> bool:
        if hasattr(self.param_type, '__origin__'):
            if self.param_type.__origin__ is Union:
                return target_type in self.param_type.__args__
            if self.param_type.__origin__ is not None:
                return issubclass(target_type, self.param_type.__origin__)
        return issubclass(target_type, self.param_type)


class ComputeField(Field):

    __slots__ = ('compute_function', 'cacheable', 'stored')

    def __init__(
            self, compute_function, cacheable: bool = False,
            stored: bool = False, **kwargs) -> None:
        """
        :param compute_function: Make field computable and use this function to calculate field value.  Default value is False
        :param cacheable: If false, field value will be recomputed every time on access. Default value is True.
        :param stored: Make field stored in database, if field computed, default False
        """
        super().__init__(**kwargs)
        self.compute_function = compute_function
        self.cacheable = cacheable
        self.stored = stored
        self.param_type = compute_function.__annotations__.get('return', Any)

    def _compute_value(self, instance):
        result = self.compute_function(instance)
        if inspect.iscoroutine(result):
            result = asyncio.ensure_future(result)
        return result

    def _compute_get_logic(self, instance):
        if not self.cacheable:
            return self._compute_value(instance)
        result = instance._values.get(self.name)
        if result is None:
            result = self._compute_value(instance)
            instance._values[self.name] = result
        return result

    def __get__(self, instance, instance_type):
        if instance is None:
            return self._query_row
        return self._compute_get_logic(instance)

    def __set__(self, instance, value) -> None:
        if not self.stored:
            raise ValueError("You cannot set value to not stored compute field")
        if not self.cacheable:
            raise ValueError("You cannot properly set not cacheable field")
        if not _type_check(value, self.param_type):
            raise ValueError(f'Field {self.name} value should have {str(self.param_type)} type instead of {value}')
        instance._values[self.name] = value

    @property
    def is_setable(self) -> bool:
        return self.stored and self.cacheable


def compute_field(
        func: Callable = None, **kwargs) -> Callable:
    """
    Very simple method to mark function that should be converted to ComputeField
    """
    if func is None:
        return functools.partial(compute_field, **kwargs)
    func._anji_compute_field = True  # type: ignore
    func._anji_compute_field_kwargs = kwargs  # type: ignore
    return func
