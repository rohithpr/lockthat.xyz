from misc.constants import HOBBY_TIER, LOCAL_STAGE, PROD_STAGE
from pynamodb.attributes import JSONAttribute, UnicodeAttribute
from pynamodb.models import Model

from .config import ACCOUNTS_TABLE, STAGE, USERS_TABLE


class Account(Model):
    class Meta:
        table_name = ACCOUNTS_TABLE
        if STAGE == LOCAL_STAGE:
            host = "http://localhost:8000"
        elif STAGE == PROD_STAGE:
            region = "us-east-1"

    uid = UnicodeAttribute(hash_key=True)
    resources = JSONAttribute(default=dict)
    plan = UnicodeAttribute(default=HOBBY_TIER)


class User(Model):
    class Meta:
        table_name = USERS_TABLE
        if STAGE == LOCAL_STAGE:
            host = "http://localhost:8000"
        elif STAGE == PROD_STAGE:
            region = "us-east-1"

    def get_id(self):
        return self.uid

    uid = UnicodeAttribute(hash_key=True)
    account_id = UnicodeAttribute()
