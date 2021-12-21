import sentry_sdk
from flask import Flask, request
from misc import constants, exceptions
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=constants.SENTRY_DSN,
    environment=constants.STAGE,
    integrations=[FlaskIntegration(), AwsLambdaIntegration()],
    traces_sample_rate=0,
)

app = Flask(__name__)


@app.route("/api/slack", methods=["GET", "POST"])
def slack():
    form_data = request.form
    token = form_data.get("token")

    if token != constants.SLACK_VERIFICATION_TOKEN:
        exceptions.capture_exception(exceptions.SlackTokenMismatch(token))
        return "Slack request token could not be verified. Please try again later."

    return {}


@app.route("/api")
def hello():
    return "Hello!"


if __name__ == "__main__":
    app.run(debug=True)
