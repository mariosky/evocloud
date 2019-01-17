from google.cloud import pubsub_v1
from google.api_core.exceptions import *
from time import sleep


project_id = "evocloud"
topic_names = ["evolved-population-objects", "population-objects"]

publisher = pubsub_v1.PublisherClient()


def create_topics(project_id, topic_names):
    for topic_name in topic_names:
        topic_path = publisher.topic_path(project_id, topic_name)
        topic = None
        try:
            topic = publisher.create_topic(topic_path)
        except AlreadyExists :
            print('Topic exists already: {}'.format(topic_path))
        if topic:
            print('Topic {} created'.format(topic))


def delete_topics(project_id, topic_names):
    for topic_name in topic_names:
        topic_path = publisher.topic_path(project_id, topic_name)
        topic_deleted = True
        try:
            publisher.delete_topic(topic_path)

        except NotFound:
            topic_deleted = False

        if topic_deleted:
            print('Topic deleted: {}'.format(topic_path))
        else:
            print('Topic {} not found'.format(topic_path))


if __name__ == '__main__':
    print("Delete topics")
    delete_topics(project_id, topic_names)
    print("Waiting 20 seconds")
    sleep(20)
    create_topics(project_id, topic_names)




