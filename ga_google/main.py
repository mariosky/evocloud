from ga_deap import *
from google.cloud import pubsub_v1
import json

## Prototipe implemantation as an OpenWhisk action,
## This function is triggered by MessageHub

project_id = "evocloud"
topic_name = "evolved-population-objects"


def main(data, context):
    # Read from MeesageHub
    if 'data' in data:
        import base64
        data_args = base64.b64decode(data['data'])
        args = json.loads(data_args)


        worker = GA_Worker(args)
        worker.setup()
        result = worker.run()

        # Return with a format for writing to MessageHub
        #
        #return { 'value' : json.dumps(result)}
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)

        data = json.dumps(result).encode('utf-8')
        publisher.publish(topic_path,data=data)

        return 'Finished'
    else:
        return 'No data'






