import os

from google.cloud import pubsub


class Publisher:
    class __Publisher:
        def __init__(self):
            self.publish_client = pubsub.PublisherClient()

    instance = None

    def __init__(self):
        if not Publisher.instance:
            Publisher.instance = Publisher.__Publisher()

    def publish_messages(self, topic, messages=None, message=None):
        topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.environ.get("PROJECT"),
            topic=topic,
        )
        if messages:
            for message in messages:
                self.publish_client.publish(topic_name, message)
        elif message:
            self.publish_client.publish(topic_name, message)

    def __getattr__(self, name):
        return getattr(self.instance, name)
