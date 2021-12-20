import os

from misc import constants

# Stages
STAGE = os.environ.get("HOLD_STAGE", "local")

# DB
PREFIX = f"{constants.PROJECT}-{STAGE}-"
ACCOUNTS_TABLE = f"{PREFIX}Accounts"
USERS_TABLE = f"{PREFIX}Users"
