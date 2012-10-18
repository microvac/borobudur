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
            if m['type'] == 'message':
                if m["channel"].startswith("/model/"):
                    data = loads(m['data'])
                    url = m["channel"][7:]
                    self.emit("model_change", url, data)

    def on_subscribe_model(self, url):
        channel = "/model/%s" % url
        self.pubsub.subscribe(channel)
        print "subscribed to %s" % url

    def on_unsubscribe_model(self, url):
        channel = "/model/%s" % url
        self.pubsub.unsubscribe(channel)
        print "unsubscribed from %s" % url

def socketio_service(request):
    retval = socketio_manage(request.environ,
        {
            '/model': ModelNamespace,
            }, request=request
    )

    return Response("", status=200)
