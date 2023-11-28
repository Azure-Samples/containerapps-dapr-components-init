import time
import requests
import os

base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
    'DAPR_HTTP_PORT', '3500')
pubsub_name = os.getenv('DAPR_PUBSUB_COMPONENT', 'pubsub')
TOPIC = 'orders'
print('Publishing to pubsub: ' + pubsub_name + ' topic: ' + TOPIC, flush=True)
print('base_url: ' + base_url, flush=True)

for i in range(1, 100):
    order = {'orderId': i}

    # Publish an event/message using Dapr PubSub via HTTP Post
    result = requests.post(
        url='%s/v1.0/publish/%s/%s' % (base_url, pubsub_name, TOPIC),
        json=order
    )

    print('Published order: %s, status code: %s' %
          (order, result.status_code), flush=True)

    time.sleep(1)
