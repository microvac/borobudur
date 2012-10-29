import gevent
from pyramid.response import Response

__author__ = 'h'
import redis
from json import loads
from json import dumps

from json import loads
from json import dumps

from socketio.mixins import RoomsMixin
from socketio.namespace import BaseNamespace
from socketio import socketio_manage

class ModelNamespace(BaseNamespace):

    def initialize(self):
        r = redis.StrictRedis()
        self.collection_subscriptions = {}
        self.pubsub = r.pubsub()
        self.spawn(self.listener)

    def listener(self):
        self.pubsub.subscribe("dummy")
        for m in self.pubsub.listen():
            if m['type'] == 'message' or m["type"] == 'pmessage':
                print "got %s %s" % (m["channel"], m["data"])
                if m["channel"].startswith("/model/"):
                    data = loads(m['data'])
                    url = m["channel"][7:]
                    self.emit("model_change", url, data)
                elif m["channel"].startswith("/collection/"):
                    data = loads(m['data'])
                    pattern = m["pattern"][12:]
                    self.emit("collection_add", pattern, data)
                    print "emitting"

    def on_subscribe_model(self, url):
        channel = "/model/%s" % url
        self.pubsub.subscribe(channel)
        print "subscribed to %s" % url

    def on_unsubscribe_model(self, url):
        channel = "/model/%s" % url
        self.pubsub.unsubscribe(channel)
        print "unsubscribed from %s" % url

    def on_subscribe_collection(self, pattern):
        channel = "/collection/%s" % pattern
        self.pubsub.psubscribe(channel)
        print "subscribed to %s" % pattern

    def on_unsubscribe_collection(self, pattern):
        channel = "/collection/%s" % pattern
        self.pubsub.punsubscribe(channel)
        print "unsubscribed for %s" % pattern

def socketio_service(request):
    retval = socketio_manage(request.environ,
        {
            '/model': ModelNamespace,
            }, request=request
    )

    return Response("", status=200)
