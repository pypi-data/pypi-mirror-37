# pylint: disable=no-self-use

from ...core import QueryRow, BaseTransformationQueryParser

from .utils import UnqliteQuery

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['UnqliteTransformationQueryParser']


class UnqliteTransformationQueryParser(BaseTransformationQueryParser[UnqliteQuery]):

    def process_group_statement(self, db_query: UnqliteQuery, group_row: QueryRow) -> UnqliteQuery:
        raise NotImplementedError()
