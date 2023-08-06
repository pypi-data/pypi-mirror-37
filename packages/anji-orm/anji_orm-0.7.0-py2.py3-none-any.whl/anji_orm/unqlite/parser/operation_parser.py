# pylint: disable=no-self-use
from typing import Optional, Callable

from toolz import itertoolz

from ...core import (
    QueryRow, BaseOperationQueryParser, AggregationType,
    QueryChangeStatement, QueryUpdateStatement
)
from .utils import UnqliteQuery

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['UnqliteOperationQueryParser']


AGGREGATION_DICT = {
    AggregationType.max: max,
    AggregationType.min: min,
    AggregationType.sum: sum,
    AggregationType.count: itertoolz.count,
    AggregationType.avg: lambda x: sum(x) / itertoolz.count(x)
}


class UnqliteOperationQueryParser(BaseOperationQueryParser[UnqliteQuery]):

    def add_post_processing_hook(self, db_query: UnqliteQuery, hook: Callable) -> UnqliteQuery:
        db_query.add_post_hook(hook)
        return db_query

    def add_pre_processing_hook(self, db_query: UnqliteQuery, hook: Callable) -> UnqliteQuery:
        db_query.add_pre_hook(hook)
        return db_query

    def process_aggregation_statement(
            self, db_query: UnqliteQuery, aggregation_type: AggregationType,
            row: Optional[QueryRow]) -> UnqliteQuery:  # pylint: disable=unused-argument
        return self.add_post_processing_hook(db_query, AGGREGATION_DICT[aggregation_type])

    def process_change_statement(
            self, db_query: UnqliteQuery, change_statement: QueryChangeStatement) -> UnqliteQuery:
        raise NotImplementedError()

    def process_update_statement(self, db_query: UnqliteQuery, update_statement: QueryUpdateStatement) -> UnqliteQuery:  # pylint: disable=unused-argument
        raise NotImplementedError()
