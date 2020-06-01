

import sentry_sdk

# DSN="https://18562a9e8e3943088b1ca3cedf222e21@o87286.ingest.sentry.io/1435220" # python-eat
DSN="http://ba993aeb5a06420e8fec21c5d276009b@o87286.ingest.sentry.io/1435220" # python-eat test1
# DSN="https://81dff1d384484340ba71696c044ffe24@o87286.ingest.sentry.io/1316515" # flask
KEY = DSN.split('@')[0]
PROXY = 'localhost:3001'
MODIFIED_DSN_FORWARD = KEY + '@' + PROXY + '/2'
MODIFIED_DSN_SAVE = KEY + '@' + PROXY + '/3'

print("DSN", DSN)
sentry_sdk.init(
    # dsn=DSN,
    # dsn=MODIFIED_DSN_FORWARD,
    dsn=MODIFIED_DSN_SAVE,
    environment="prod",

    traces_sample_rate=1.0
)

print('HHHHHHHHHI')
obj = {}
obj['YourkeyDoesntExist']