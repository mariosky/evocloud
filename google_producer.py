import time
import os
import json
from google.cloud import pubsub_v1
import logging

logger = logging.getLogger('google_experiment')
logger.setLevel(logging.INFO)

project_id = os.environ["PROJECT_ID"]
topic_name = "population-objects"



def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        logging.info('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        logging.info("Message OUT:", message_future.result())


def send_messages(messages, project_id="evocloud",topic_name = "population-objects"):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for message in messages:
        json_data = json.dumps(message)
        # Data must be a bytestring

        data = json_data.encode('utf-8')


        # When you publish a message, the client returns a Future.
        message_future = publisher.publish(topic_path, data=data)
        message_future.add_done_callback(callback)
