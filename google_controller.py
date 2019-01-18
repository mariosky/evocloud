import json
import random
import os
import asyncio
import redis


HOST = os.environ['REDIS_HOST']
PORT = os.environ['REDIS_PORT']
REDIS_LOG = os.environ['REDIS_LOG']


r = redis.Redis(host=HOST, port=PORT)


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


def cxBestFromEach(pop1, pop2, key = lambda p: p['fitness']['score']):
    # small is better
    pop1.sort(key=key)
    pop2.sort(key=key)
    size = min(len(pop1), len(pop2))

    cxpoint = (size - 1) / 2

    pop1[cxpoint:] = pop2[:cxpoint+2]

    return pop1





queue = []
count = 0


async def print_message(message, loop, env):
    global count, queue
    await asyncio.sleep(0.1)
    message.ack()

    pop = json.loads(message.data)
    max_messages = env["problem"]["max_iterations"]

    print(max_messages)


    # Counter for experiments, some times we receive from earlier problems
    # Set to zero if not exists
    problem_id = env["problem"]["problem_id"]

    if problem_id == pop["problem"]["problem_id"]:
        queue.append(pop)

        if len(queue) > 1:
            # get other
            # other = queue.pop()
            # random from the last 10
            # percentege of length
            other = random.choice(queue)
            # crossover

            # cxOnePoint(pop['population'], other['population'])
            pop['population'] = cxBestFromEach(pop['population'], other['population'])
            # queue.appendleft(other)
            # queue.append(other)
            print('.',)

        # Only return if we are in the same experiment
        print("SEND MESSAGGE HERE")
        print(json.dumps(pop ))

        # Log any way, there is no problem if we evaluate more
        if (REDIS_LOG):
            await redis_log.log_to_redis_coco(pop)
        else:
            print("old", pop["problem"]["problem_id"])




    if count >= max_messages:
        print("stop")
        await asyncio.sleep(0.1)
        loop.stop()
        await r.rpush('experiment_finished', count)

    count+=1


def experiment(env):
    global count, queue
    count = 0
    queue = []


    loop = asyncio.get_event_loop()

    producer = pubsub_v1.PublisherClient()
    topic_path = producer.topic_path(project_id, population_objects_topic)

    def create_print_message_task(message):
        """ Callback handler for the subscription; schedule a task on the event loop """
        asyncio.run_coroutine_threadsafe(print_message(message, loop, env), loop)

    subscriber.subscribe(subscription_path, callback=create_print_message_task)

    loop.run_forever()

