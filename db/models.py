from pynamodb.attributes import BooleanAttribute, JSONAttribute, ListAttribute, UnicodeAttribute
from pynamodb.models import Model
from .config import ACCOUNTS_TABLE, USERS_TABLE, STAGE
from misc.constants import LOCAL_STAGE, PROD_STAGE


class Account(Model):
    class Meta:
        table_name = ACCOUNTS_TABLE
        if STAGE == LOCAL_STAGE:
            host = "http://localhost:8000"
        elif STAGE == PROD_STAGE:
            region = "us-east-1"
    
    uid = UnicodeAttribute(hash_key=True)
    resources = JSONAttribute(default={})


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
