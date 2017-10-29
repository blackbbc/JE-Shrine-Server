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

    def serialize_mongo_doc(self, doc):
        if '_id' in doc and isinstance(doc['_id'], ObjectId):
            doc['id'] = str(doc['_id'])
            del a['_id']
        for key in doc.keys():
            if isinstance(doc[key], ObjectId):

        return json_util._json_convert(doc)

    def default(self, obj):
        if isinstance(obj, BaseDocument):
            return self.serialize_mongo_doc(obj.to_mongo())
        elif isinstance(obj, QuerySet):
            return json_util._json_convert(obj.as_pymongo())
        return superclass.default(self, obj)
