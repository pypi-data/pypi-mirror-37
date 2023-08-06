from typing import List, Any
import logging
from datetime import datetime

import unqlite


from ..core import (
    AbstractSyncRegisterStrategy, AbstractAsyncRegisterStrategy,
    AbstractAsyncExecutor, AbstractSyncExecutor, AbstractQueryParser,
    AbstractBackendAdapter, NotSupportException
)

from .parser import UnqliteQueryParser
from .executor import UnqliteSyncExecutor, UnqliteAsyncExecutor
from .utils import serialize_datetime


__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = [
    "SyncUnqliteRegisterStrategy", "AsyncUnqliteRegisterStrategy",
    "UnqliteBackendAdapter"
]

_log = logging.getLogger(__name__)


class UnqliteBackendAdapter(AbstractBackendAdapter):

    def utcnow(self) -> datetime:
        return datetime.utcnow()

    def now(self) -> datetime:
        return datetime.now()

    def ensure_compatibility(self, value):
        if isinstance(value, datetime):
            return serialize_datetime(value).encode('utf-8')
        if isinstance(value, str):
            return value.encode('utf-8')
        return value


class SyncUnqliteRegisterStrategy(AbstractSyncRegisterStrategy):

    def __init__(self, connection_uri: str, **pool_kwargs: Any) -> None:  # pylint: disable=super-init-not-called

        self.db_connection = unqlite.UnQLite(filename=connection_uri.split('://')[1])
        self._backend_adapter = UnqliteBackendAdapter()
        self._query_parser = UnqliteQueryParser()
        self._executor = UnqliteSyncExecutor(self)

    @property
    def executor(self) -> AbstractSyncExecutor:
        return self._executor

    @property
    def query_parser(self) -> AbstractQueryParser:
        return self._query_parser

    @property
    def backend_adapter(self) -> AbstractBackendAdapter:
        return self._backend_adapter

    @property
    def db(self) -> Any:
        return self.db_connection

    def execute_query(self, query: Any) -> Any:
        raise NotSupportException("Please, use db object directly")

    def load(self) -> None:
        pass

    def create_index(
            self, table_name: str,
            index_name: str, index_fields: List[str]) -> None:
        _log.warning(
            'Unqlite backend does not support indexing, index %s will not be created',
            index_name
        )

    def drop_index(self, table_name: str, index_name: str) -> None:
        _log.warning(
            'Unqlite backend does not support indexing, index %s will not be dropped',
            index_name
        )

    def list_indexes(self, table_name: str) -> List[str]:
        return []

    def create_table(self, table_name: str) -> None:
        self.db.collection(table_name).create()

    def drop_table(self, table_name: str) -> None:
        self.db.collection(table_name).drop()

    def list_tables(self) -> List[str]:
        # Note, that in unqlite currently you cannot fetch
        # list of tables, so we will be recreated it over and over
        return []

    def close(self) -> None:
        self.db.close()


class AsyncUnqliteRegisterStrategy(AbstractAsyncRegisterStrategy):

    def __init__(self, connection_uri: str, **pool_kwargs: Any) -> None:  # pylint: disable=super-init-not-called

        self.db_connection = unqlite.UnQLite(filename=connection_uri.split('://')[1])
        self._backend_adapter = UnqliteBackendAdapter()
        self._query_parser = UnqliteQueryParser()
        self._executor = UnqliteAsyncExecutor(self)

    @property
    def executor(self) -> AbstractAsyncExecutor:
        return self._executor

    @property
    def query_parser(self) -> AbstractQueryParser:
        return self._query_parser

    @property
    def backend_adapter(self) -> AbstractBackendAdapter:
        return self._backend_adapter

    @property
    def db(self) -> Any:
        return self.db_connection

    async def execute_query(self, query: Any) -> Any:
        raise NotSupportException("Please, use db object directly")

    async def load(self) -> None:
        pass

    async def create_index(
            self, table_name: str,
            index_name: str, index_fields: List[str]) -> None:
        _log.warning(
            'Unqlite backend does not support indexing, index %s will not be created',
            index_name
        )

    async def drop_index(self, table_name: str, index_name: str) -> None:
        _log.warning(
            'Unqlite backend does not support indexing, index %s will not be dropped',
            index_name
        )

    async def list_indexes(self, table_name: str) -> List[str]:
        return []

    async def create_table(self, table_name: str) -> None:
        self.db.collection(table_name).create()

    async def drop_table(self, table_name: str) -> None:
        self.db.collection(table_name).drop()

    async def list_tables(self) -> List[str]:
        # Note, that in unqlite currently you cannot fetch
        # list of tables, so we will be recreated it over and over
        return []

    async def close(self) -> None:
        self.db.close()
