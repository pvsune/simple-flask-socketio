from flask import Flask, render_template, request
from flask_socketio import Namespace, SocketIO, emit


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
        emit('my_response', {'data': message['data']})

    def on_my_broadcast_event(self, message):
        emit('my_response', {'data': message['data']}, broadcast=True)

ns = MyCustomNamespace('/test')
socketio.on_namespace(ns)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook')
def webhook():
    data = {'data': 'This message is initiated from server.'}
    socketio.emit('my_response', data, namespace='/test', room=ns.room)
    return 'OK'


if __name__ == '__main__':
    socketio.run(app)
