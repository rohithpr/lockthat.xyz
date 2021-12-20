# WARNING - not really constants... constant for a given session.

import os

# Stages
STAGE = os.environ.get("HOLD_STAGE", "local")

PROJECT = "takethat"

LOCAL_STAGE = "local"
PROD_STAGE = "prod"

HOBBY_TIER = "hobby"

HOBBY_TIER_RESOURCE_LIMIT = 50

# Sentry
SENTRY_DSN = os.environ.get("HOLD_SENTRY_DSN")
