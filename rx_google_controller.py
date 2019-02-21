from rx import Observable
from rx.subjects import Subject
import redis
import logging
import google_producer
import redis_log
import os
import json
import random
import sys
import time

from google.cloud import pubsub_v1

def cxBestFromEach(pop1, pop2, key = lambda p: p['fitness']['score']):

    # small is better
    pop1.sort(key=key)
    pop2.sort(key=key)
    size = min(len(pop1), len(pop2))

    cxpoint = (size - 1) // 2

    pop1[cxpoint:] = pop2[:cxpoint+2]
    return pop1





class GooglePubSubExperiment():
    def __init__(self, env):
        self.env = env
        self.consumed_messages = Subject()
        self.messages = Subject()

        self.project_id = os.environ["PROJECT_ID"]
        self.population_objects_topic = "population-objects"
        self.subscription_name = "evolved-subscription"
        self.google_subscriber =  pubsub_v1.SubscriberClient()
        self.subscription_path = self.google_subscriber.subscription_path( self.project_id, self.subscription_name)

        self.google_subscriber.subscribe(self.subscription_path, callback=self.callback_message)
        self.consumed_messages\
            .take(env["problem"]["max_iterations"])\
            .buffer_with_count(3)\
            .subscribe( on_next=lambda x : self.population_mixer(x),on_completed = self.finish)

        self.consumed_messages.subscribe(lambda x : print('CONSUMED:{}'.format(x)),on_completed = lambda :"MESSAGES COMPLETED"  )
        self.messages.publish()

        self.messages.subscribe(lambda populations : google_producer.send_messages(populations), on_completed = lambda :"MESSAGES COMPLETED" )

    def finish(self):

        print("Finished")
        self.messages.on_completed()
        self.messages.dispose()
        sys.exit(0)


    def callback_message(self,message):
        message.ack()

        self.consumed_messages.on_next(message)

    def population_mixer(self, populations):
        if len(populations) == 3:
            print("MIXER",populations[0])
            populations = [json.loads(message.data) for message in populations]
            populations[0]['population'] = cxBestFromEach(populations[0]['population'],populations[1]['population'])
            populations[1]['population'] = cxBestFromEach(populations[1]['population'], populations[2]['population'])
            populations[2]['population'] = cxBestFromEach(populations[2]['population'], populations[0]['population'])

        self.messages.on_next(populations[0])







GooglePubSubExperiment({"problem":{"max_iterations":6}})
time.sleep(4)



