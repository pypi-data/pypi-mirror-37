from datetime import datetime
from typing import Dict, Optional

from anji_orm import Model, Field, IndexPolicy, IndexPolicySetting


class T1(Model):

    _table = 'test_table'

    _index_policy = IndexPolicy.singlemore
    _index_policy_settings = {
        IndexPolicySetting.additional_indexes: [
            ('c1:c2', ['c1', 'c2'])
        ]
    }

    c1: Optional[str] = Field(secondary_index=True)
    c2: Optional[str] = Field(secondary_index=True)
    c3: Optional[datetime]
    c4: Optional[Dict]
    c5: Optional[str]
