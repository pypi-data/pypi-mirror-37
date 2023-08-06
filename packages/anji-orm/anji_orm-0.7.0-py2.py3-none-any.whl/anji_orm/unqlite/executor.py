from typing import Optional, Dict, Type, Tuple, List
from datetime import datetime
import logging
from importlib import import_module
import operator

from toolz.itertoolz import isiterable

from ..core import (
    AbstractAsyncExecutor, AbstractSyncExecutor, Model, fetch
)
from .utils import (
    unqlite_dict_deserialize, unqlite_dict_serialize
)

from .parser.utils import UnqliteQuery

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = ["UnqliteSyncExecutor", "UnqliteAsyncExecutor"]

_log = logging.getLogger(__name__)


def unqlite_fetch(obj_data):
    if '_python_info' not in obj_data:
        # Return just this dict, if he cannot be recognized as orm model
        return obj_data
    python_info = obj_data.pop('_python_info')
    class_module = import_module(python_info['module_name'].decode())
    class_object = getattr(class_module, python_info['class_name'].decode(), None)
    if class_object is None:
        _log.warning('Model record %s cannot be parsed, because class wasnt found!', obj_data['__id'])
        return None
    unqlite_dict_deserialize(class_object, obj_data)
    obj = class_object(**obj_data)
    return obj


def process_driver_response(result):
    if isinstance(result, dict):
        return unqlite_fetch(result)
    if isiterable(result):
        return filter(
            operator.truth,
            (
                unqlite_fetch(obj_data)
                if isinstance(obj_data, dict) else obj_data
                for obj_data in result
            )
        )
    return result


class UnqliteModel:

    __slots__: List[str] = []

    @staticmethod
    def pre_put(model: Model) -> Dict:
        model.orm_last_write_timestamp = datetime.now()
        model_dict = model.to_dict()
        unqlite_dict_serialize(model.__class__, model_dict)
        return model_dict

    @staticmethod
    def post_put(model: Model, result: int) -> None:
        if model.id is None:
            try:
                model.id = str(result)
            except ValueError as exc:
                _log.warning(
                    'Strange error %s when processing put result %s',
                    exc, result
                )

    @staticmethod
    def post_get(model_cls: Type[Model], model_dict: Dict) -> Dict:
        unqlite_dict_deserialize(model_cls, model_dict)
        return model_dict


class QueryExecution:

    __slots__: List[str] = []

    @staticmethod
    def post_execution(execution_result, query: UnqliteQuery, without_fetch: bool):
        if query.pre_hooks:
            for pre_hook in query.pre_hooks:
                execution_result = pre_hook(execution_result)
        if not without_fetch:
            execution_result = process_driver_response(execution_result)
        if query.post_hooks:
            for post_hook in query.post_hooks:
                execution_result = post_hook(execution_result)
        return execution_result


class UnqliteSyncExecutor(AbstractSyncExecutor[UnqliteQuery]):

    def send_model(self, model: Model) -> Dict:
        model_dict = UnqliteModel.pre_put(model)
        if model.id:
            result = self.strategy.db.collection(model._table).update(model.id, model_dict)
        else:
            result = self.strategy.db.collection(model._table).store(model_dict)
        UnqliteModel.post_put(model, result)
        return result

    def load_model(self, model: Model) -> Tuple[Dict, Optional[Dict]]:
        if model.id is None:
            raise ValueError("Cannot load model without id")
        model_dict = self.strategy.db.collection(model._table).fetch(model.id)
        return UnqliteModel.post_get(model.__class__, model_dict), {}

    def delete_model(self, model: Model) -> Dict:
        if model.id is None:
            raise ValueError("Cannot load model without id")
        return self.strategy.db.collection(model._table).delete(model.id)

    def get_model(self, model_cls: Type[Model], id_) -> Optional[Model]:
        model_dict = self.strategy.db.collection(model_cls._table).fetch(id_)
        record = fetch(UnqliteModel.post_get(model_cls, model_dict))
        return record

    def execute_query(self, query: UnqliteQuery, without_fetch: bool = False):
        if query.filter_function is not None:
            execution_result = self.strategy.db.collection(query.table).filter(
                query.filter_function
            )
        else:
            execution_result = self.strategy.db.collection(query.table).all()
        return QueryExecution.post_execution(execution_result, query, without_fetch)


class UnqliteAsyncExecutor(AbstractAsyncExecutor[UnqliteQuery]):

    async def send_model(self, model: Model) -> Dict:
        model_dict = UnqliteModel.pre_put(model)
        if model.id:
            result = self.strategy.db.collection(model._table).update(model.id, model_dict)
        else:
            result = self.strategy.db.collection(model._table).store(model_dict)
        UnqliteModel.post_put(model, result)
        return result

    async def load_model(self, model: Model) -> Tuple[Dict, Optional[Dict]]:
        if model.id is None:
            raise ValueError("Cannot load model without id")
        model_dict = self.strategy.db.collection(model._table).fetch(model.id)
        return UnqliteModel.post_get(model.__class__, model_dict), {}

    async def delete_model(self, model: Model) -> Dict:
        if model.id is None:
            raise ValueError("Cannot load model without id")
        return self.strategy.db.collection(model._table).delete(model.id)

    async def get_model(self, model_cls: Type[Model], id_) -> Optional[Model]:
        model_dict = self.strategy.db.collection(model_cls._table).fetch(id_)
        record = fetch(UnqliteModel.post_get(model_cls, model_dict))
        return record

    async def execute_query(self, query: UnqliteQuery, without_fetch: bool = False):
        if query.filter_function is not None:
            execution_result = self.strategy.db.collection(query.table).filter(
                query.filter_function
            )
        else:
            execution_result = self.strategy.db.collection(query.table).all()
        return QueryExecution.post_execution(execution_result, query, without_fetch)
