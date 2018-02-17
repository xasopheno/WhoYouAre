import socketio
import eventlet
from flask import Flask
import random

sio = socketio.Server(logger=True, async_mode=None)
app = Flask(__name__)


class Counter:
    def __init__(self):
        self.count = 0

    def inc(self):
        self.count += 1

counter = Counter()


@sio.on('connect')
def connect(sid, environ):
    print('client_connect', sid)
    sio.emit('connected_to_server', {'message': 'Connected', 'count': counter.count})
    counter.count += 1
    print(counter.count)


def prepare_payload(freq):
    payload = {
        'freq': freq,
        'vol': 100
    }
    return payload


@sio.on('freq_change')
def freq_change(sid, data):
    freq = data['freq']

    output = prepare_payload(freq)
    sio.emit('freq', output)


@sio.on('echo')
def message(sid, data):
    print('echo')
    rand = random.randint(100, 1000)
    payload = prepare_payload(rand)

    sio.emit('freq', payload)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

app = socketio.Middleware(sio, app)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 9876)), app)
