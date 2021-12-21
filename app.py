import sentry_sdk
from flask import Flask, request
from misc import constants
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=constants.SENTRY_DSN,
    environment=constants.STAGE,
    integrations=[FlaskIntegration(), AwsLambdaIntegration()],
    traces_sample_rate=0,
)

app = Flask(__name__)


@app.route("/slack/command", methods=["GET", "POST"])
def hello():
    print(request.data)
    return {}


if __name__ == "__main__":
    app.run(debug=True)
