from flask import Flask, request, jsonify
import json
import os

import requests

app = Flask(__name__)

base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
    'DAPR_HTTP_PORT', '3500')
statestore_name = os.getenv('DAPR_STATESTORE_COMPONENT', 'statestore')
pubsub_name = os.getenv('DAPR_PUBSUB_COMPONENT', 'pubsub')
app_port = os.getenv('APP_PORT', '6001')


@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    """Register Dapr pub/sub subscriptions"""
    subscriptions = [{
        'pubsubname': pubsub_name,
        'topic': 'orders',
        'route': 'orders'
    }]
    print('Dapr pub/sub is subscribed to: ' +
          json.dumps(subscriptions), flush=True)
    return jsonify(subscriptions)


@app.route('/orders', methods=['POST'])
def orders_subscriber():
    """Dapr subscription in /dapr/subscribe sets up this route"""
    order = request.json['data']
    print('Subscriber received : ' + json.dumps(order), flush=True)

    state_data = [{
        "key": "order",
        "value": order
    }]

    # Save the orderid to statestore
    result = requests.post(
        url='%s/v1.0/state/%s' % (base_url, statestore_name),
        json=state_data,
    )
    print('Statestore response: ' + result.text, flush=True)

    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_port)
