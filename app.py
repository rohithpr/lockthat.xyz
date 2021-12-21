import sentry_sdk
from flask import Flask, request
from misc import constants, exceptions
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from service import account_service, command_service

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
    text = form_data.get("text")
    account_id = form_data.get("team_id")
    user = form_data.get("user_id")

    if token != constants.SLACK_VERIFICATION_TOKEN:
        exceptions.capture_exception(exceptions.SlackTokenMismatch(token))
        return "Slack request token could not be verified. Please try again later."

    account = account_service.get_or_create_account(account_id)
    target_method, kwargs = command_service.parse_command(text)
    try:
        return target_method(account=account, user=user, **kwargs)
    except exceptions.HoldException as e:
        return e.message
    except Exception:
        return "An unknown error occurred. Please try again later or contact us at letsfinditio@gmail.com."


@app.route("/api")
def hello():
    return "Hello!"


if __name__ == "__main__":
    app.run(debug=True)
