from typing import Dict, Type
from datetime import datetime

from ..core import Model

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = [
    "serialize_datetime", "deserialize_datetime",
    "unqlite_dict_serialize", "unqlite_dict_deserialize"
]

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def unqlite_dict_serialize(model: Type[Model], model_dict: Dict) -> None:
    # Unqlite don't need id to control
    model_dict.pop('id', None)
    for field_name, field in model._fields.items():
        if field.can_be(datetime) and field_name in model_dict:
            if isinstance(model_dict[field_name], datetime):
                model_dict[field_name] = serialize_datetime(model_dict[field_name])


def unqlite_dict_deserialize(model: Type[Model], model_dict: Dict) -> None:
    model_dict['id'] = str(model_dict.pop('__id'))
    for field_name, field in model._fields.items():
        if field_name in model_dict:
            if field.can_be(dict) and isinstance(model_dict[field_name], list):
                # WHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAT!!!
                # Empty dict will become empty array in this database!
                if model_dict[field_name]:
                    raise ValueError('Well ... how does this happend?')
                model_dict[field_name] = dict()
            if field.can_be(str) and isinstance(model_dict[field_name], bytes):
                model_dict[field_name] = model_dict[field_name].decode()
            if field.can_be(datetime):
                if isinstance(model_dict[field_name], bytes):
                    model_dict[field_name] = deserialize_datetime(model_dict[field_name].decode())
                if isinstance(model_dict[field_name], str):
                    model_dict[field_name] = deserialize_datetime(model_dict[field_name])


def serialize_datetime(value: datetime) -> str:
    return value.strftime(DATETIME_FORMAT)


def deserialize_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)
