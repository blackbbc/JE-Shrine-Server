from functools import singledispatch
from datetime import datetime

from bson import json_util
from bson.objectid import ObjectId
from flask.json import JSONEncoder

from mongoengine.base import BaseDocument
from mongoengine.queryset import QuerySet

class MongoJSONEncoder(JSONEncoder):
    """
    A JSONEncoder which provides serialization of MongoEngine
    documents and queryset objects.
    """

    def default(self, obj):
        """
        Convert the object into JSON-serializable value.
        Parameters:
            obj: Object to be converted.
        """

        @singledispatch
        def convert(obj):
            print('default')
            return JSONEncoder.default(self, obj)

        @convert.register(ObjectId)
        def _(obj):
            return str(obj)

        @convert.register(datetime)
        def _(obj):
            return int(obj.timestamp())

        @convert.register(BaseDocument)
        def _(obj):
            doc = obj.to_mongo()
            if '_id' in doc and isinstance(doc['_id'], ObjectId):
                doc['id'] = doc.pop('_id')
            return doc

        @convert.register(QuerySet)
        def _(obj):
            docs = [ doc for doc in obj ]
            return docs

        return convert(obj)
