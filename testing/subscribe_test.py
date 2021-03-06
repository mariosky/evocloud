import time
import json
from rx.subjects import Subject

from google.cloud import pubsub_v1

project_id = "evocloud"
subscription_name = "evolved-subscription"

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(project_id, subscription_name)


events = Subject()

def callback(message):
    print('Received message: {}'.format(message))
    data_dic = json.loads(message.data)
    print(data_dic['problem'])
    events.on_next(message)
    message.ack()




subscriber.subscribe(subscription_path, callback=callback)

events.subscribe(lambda message: print('msssssss:'))

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)