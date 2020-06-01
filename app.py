import os
from flask import Flask, request, json, abort
from flask_cors import CORS

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

DSN="https://18562a9e8e3943088b1ca3cedf222e21@o87286.ingest.sentry.io/1435220" # python-eat
# DSN="http://18562a9e8e3943088b1ca3cedf222e21@o87286.ingest.sentry.io/1435220" # python-eat

# DSN="http://09aa0d909232457a8a6dfff118bac658@localhost:9000/2" # flask
KEY = DSN.split('@')[0]
PROXY = 'localhost:3001'
MODIFIED_DSN_FORWARD = KEY + '@' + PROXY + '/2'
MODIFIED_DSN_SAVE = KEY + '@' + PROXY + '/3'

"""
sentry-sdk[flask]==0.9.5 (June28th, 2019)
replaced by
sentry-sdk==0.14.4 
"""
print('\nDSN', DSN)
sentry_sdk.init(
    dsn=DSN,
    # dsn=MODIFIED_DSN_FORWARD,
    # dsn=MODIFIED_DSN_SAVE,
    integrations=[FlaskIntegration()],
    release=os.environ.get("VERSION"),
    environment="prod",

    traces_sample_rate=1.0
)

app = Flask(__name__)
CORS(app)

@app.route('/handled', methods=['GET'])
def handled_exception():
    with sentry_sdk.start_span(op="app.route.handled1"):
        try:
            # print('hello')
            '2' + 2
        except Exception as err:
            print('EEEEEEEEEEEEEEEEEEEEEe')
            # print(err)
            sentry_sdk.capture_exception(err)
            # abort(500)
    return 'Sucasdfcey'

@app.route('/unhandled', methods=['GET'])
def unhandled_exception():
    obj = {}
    obj['ThisDoesntExist']

Inventory = {
    'wrench': 1,
    'nails': 1,
    'hammer': 1
}

def process_order(cart):
    global Inventory
    tempInventory = Inventory
    for item in cart:
        if Inventory[item['id']] <= 0:
            raise Exception("Not enough inventory for " + item['id'])
        else:
            tempInventory[item['id']] -= 1
            print('Success: ' + item['id'] + ' was purchased, remaining stock is ' + str(tempInventory[item['id']]))
    Inventory = tempInventory 

@app.before_request
def sentry_event_context():
    # with sentry_sdk.start_span(op="app.before_request"):
    if (request.data):
        order = json.loads(request.data)
        with sentry_sdk.configure_scope() as scope:
                scope.user = { "email" : order["email"] }
        
    transactionId = request.headers.get('X-Transaction-ID')
    sessionId = request.headers.get('X-Session-ID')
    global Inventory

    with sentry_sdk.configure_scope() as scope:
        # scope.set_tag("transaction_id", transactionId)
        # scope.set_tag("session-id", sessionId)
        scope.set_extra("inventory", Inventory)

@app.route('/checkout', methods=['POST'])
def checkout():
    with sentry_sdk.start_span(op="app.checkout"):
        order = json.loads(request.data)
        print("Processing order for: " + order["email"])
        cart = order["cart"]
        
        process_order(cart)

        return 'Success'