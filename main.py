from flask import Flask, render_template
from flask_socketio import SocketIO, emit, Namespace

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, engineio_logger=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cb')
def cb():
   socketio.emit('my_response', {'data': 42}, namespace='/test')
   return '200 OK'


class MyCustomNamespace(Namespace):
    def on_connect(self):
        emit('my_response', {'data': 'Connected'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_my_event(self, message):
        emit('my_response', {'data': message['data']})

    def on_my_broadcast_event(self, message):
        emit('my_response', {'data': message['data']}, broadcast=True)

socketio.on_namespace(MyCustomNamespace('/test'))


if __name__ == '__main__':
    socketio.run(app)
