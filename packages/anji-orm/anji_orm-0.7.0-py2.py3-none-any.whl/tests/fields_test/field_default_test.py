from anji_orm import Model
from ..base import BaseTestCase


class T1(Model):

    _table = 'non_table'

    c1: str = '5'


class FieldValidationTest(BaseTestCase):

    def test_simple_default(self) -> None:
        test_record = T1()
        self.assertEqual(test_record.c1, '5')
