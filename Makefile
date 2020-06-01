# Must have `sentry-cli` installed globally
# Following variable must be passed in:

SENTRY_AUTH_TOKEN=ec90530d75284c30a82b3695b051bb5ca6456235a72044ac8fbc3fa5d4563249

SENTRY_ORG_SELF_HOSTED=sentry
SENTRY_PROJECT_SELF_HOSTED=flask

SENTRY_ORG=testorg-az
SENTRY_PROJECT=flask
VERSION=`sentry-cli releases propose-version`

deploy: create_release run_flask

create_release:
	sentry-cli releases -o $(SENTRY_ORG) new -p $(SENTRY_PROJECT) $(VERSION)

# makes Sentry look at commits sitting on Sentry, and associates them to this Release that's getting pushed up
associate_commits:
	sentry-cli --url http://localhost:9000 releases -o $(SENTRY_ORG) -p $(SENTRY_PROJECT) set-commits --auto $(VERSION)

run_flask:
	VERSION=$(VERSION) FLASK_APP=app.py flask run -p 3002
