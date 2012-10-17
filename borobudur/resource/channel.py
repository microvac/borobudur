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
        self.pubsub = r.pubsub()
        self.spawn(self.listener)

    def listener(self):
        self.pubsub.subscribe("dummy")
        for m in self.pubsub.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                self.emit("model", m["channel"], data)

    def on_subscribe(self, url):
        self.pubsub.subscribe(url)
        print "subscribed to %s" % url

    def on_unsubscribe(self, url):
        self.pubsub.unsubscribe(url)
        print "unsubscribed from %s" % url


def socketio_service(request):
    retval = socketio_manage(request.environ,
        {
            '/model': ModelNamespace,
            }, request=request
    )
    print "writing response?"

    return Response("", status=200)
