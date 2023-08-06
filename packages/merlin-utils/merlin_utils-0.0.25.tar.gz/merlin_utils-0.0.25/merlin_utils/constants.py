import os

from google.cloud import datastore


class Constants:
    class __Constants:
        def __init__(self):
            datastore_client = datastore.Client(os.environ.get("PROJECT"))
            query = datastore_client.query(kind="Params")
            query.add_filter("status", "=", "ACTIVE")
            constants = {}
            for entity in list(query.fetch()):
                value = entity.get("langValues", entity.get("value"))
                constants[entity["name"]] = value
            self.constants = constants

    instance = None

    def __init__(self):
        if not Constants.instance:
            Constants.instance = Constants.__Constants()

    def get_constant(self, key, language="en"):
        constant = self.constants.get(key)
        if constant is not None:
            return constant.get(language) if isinstance(constant, dict) else constant

    def __getattr__(self, name):
        return getattr(self.instance, name)
