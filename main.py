from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, Namespace

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, engineio_logger=True)


class MyCustomNamespace(Namespace):
    room = None

    def on_connect(self):
        self.room = request.sid
        emit('my_response', {'data': 'Connected'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_my_event(self, message):
        emit('my_response', {'data': self.room})

    def on_my_broadcast_event(self, message):
        emit('my_response', {'data': message['data']}, broadcast=True)

t = MyCustomNamespace('/test')
socketio.on_namespace(t)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cb')
def cb():
    socketio.emit('my_response', {'data': t.room}, namespace='/test', room=t.room)
    return '200 OK'


if __name__ == '__main__':
    socketio.run(app)
