import json
import random
import os
import asyncio



from google.cloud import pubsub_v1

import redis_log
from deap.tools.crossover import cxOnePoint

project_id = os.environ["PROJECT_ID"]
population_objects_topic = "population-objects"
subscription_name = "evolved-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    project_id, subscription_name)

print(subscription_path)





count = 0

async def print_message(message, loop):
    await asyncio.sleep(0.1)

    print('Received message: {}'.format(message))
    data_dic = json.loads(message.data)
    print(data_dic['problem'])
    global count
    print(count)
    message.ack()
    if count >= 2:
        print("stop")
        await asyncio.sleep(0.1)
        loop.stop()
    count+=1


def experiment(env):
    global count
    count = 0
    loop = asyncio.get_event_loop()

    producer = pubsub_v1.PublisherClient()
    topic_path = producer.topic_path(project_id, population_objects_topic)

    def create_print_message_task(message):
        """ Callback handler for the subscription; schedule a task on the event loop """
        #loop.create_task(print_message(message, loop))
        asyncio.run_coroutine_threadsafe(print_message(message, loop), loop)

    subscriber.subscribe(subscription_path, callback=create_print_message_task)

    max_messages = env["problem"]["max_iterations"]


    # Counter for experiments, some times we receive from earlier problems
    # Set to zero if not exists
    problem_id = env["problem"]["problem_id"]
    queue = []

    loop.run_forever()

