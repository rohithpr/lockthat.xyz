# LockThat

## Resource Usage Manager for Slack

Want to try the hosted version of this app? Install it to your Slack account from [lockthat.xyz](https://lockthat.xyz).

### Project Summary

Use LockThat to keep track of your team's shared resources and who is using them. No more pesky messages like "Is anyone using the test site?", just run `/lockthat lock test-site` and you'll either get to use the test site or you'll get to know who is using it. Run `/lockthat help` to learn more about the app.

Note: LockThat does not prevent multiple people from using the same resource. It works on an honor system!

### Example Slack Commands

- `/lockthat help`: Display help text with information about all the commands you can use with LockThat.
- `/lockthat create test-site`: Register a new resource called `test-site`.
- `/lockthat lock test-site`: Lock `test-site` for your use for 24 hours.
- `/lockthat lock test-site 12 d super secret project`: Lock `test-site` for 12 days, along with a message about why you're using it. You can also lock a resource for other specific periods of time. Eg: 30 days, 2 hours, 5 weeks, or 1 month.
- `/lockthat unlock test-site`: Unlock `test-site` and make it available for others to use.
- `/lockthat delete test-site`: Deregister `test-site` from the LockThat app.
- `/lockthat list`: Get a list of all the resources registered with LockThat.

### Run the project locally

- Install dependencies: `pip install -r requirements/local.txt`.
- Run DynamoDB: `docker compose up -d`.
- Start the webserver: `python app.py`.
- Run tests: `pytest`

### Instructions to self host

#### Commands to setup the backend on AWS

- Install and setup [Serverless](https://serverless.com/)
- Install node dependencies listed in [package.json](./package.json) required by Serverless.
- Configure the following environment variables:
  - Values obtained while registering the Slack app:
    - `HOLD_SLACK_VERIFICATION_TOKEN` - Slack verification token
    - `HOLD_SLACK_SIGNING_SECRET` - Slack signing secret
    - `HOLD_SLACK_CLIENT_ID` - Slack client id
    - `HOLD_SLACK_CLIENT_SECRET` - Slack client secret
  - Values obtained while registering the Sentry app:
    - `HOLD_SENTRY_DSN` - Sentry DSN

- `sls create_domain` to create the specified domain on AWS.
- `sls deploy --stage prod` to update the CF stack.
- `sls deploy function --function app --stage prod` to update just the function code without any infra changes.

#### Register Slack app

- TODO

### Registering Sentry app

- TODO

### TODO

- Run the webserver in a Docker container for local development.
- Add instructions in README on how to set up a custom Slack app for self hosted backend.
- Improve test coverage and set up Github actions to run tests.
- Add documentation & OpenAPI specs related to supported endpoints.
