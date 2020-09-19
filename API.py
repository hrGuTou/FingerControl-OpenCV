from flask import Flask
from flask_socketio import SocketIO, send, emit
import base64
import numpy as np
import cv2
from Detector.GestureDetector import FingerControl
from flask_cors import CORS, cross_origin
import eventlet
movements = {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right"
    }
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yigeiwoligiao!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# @app.route('/')
# @ cross_origin()
# def site():
#     return "HI"

@socketio.on('frame')
#@cross_origin()
def handler(payload):
    b64 = payload['b64']
    status = payload['status']
    width = payload['width']
    height = payload['height']
    #print(width, " ", height)

    #fingerControl = FingerControl(x0=int(width*(5/32)), y0=int(height*(5/18)), x1=int(width*(15/32)), y1=int(height*(5/6)), movements=movements)
    fingerControl = FingerControl(x0=100, y0=700, x1=100, y1=700, movements=movements)
    try:
        img = base64.b64decode(b64)
        img = np.array(list(img))
        img_array = np.array(img, dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        #print(frame)
        #cv2.imshow("test", frame)
        #cv2.waitKey(20)

        imout, res = fingerControl.startStream(frame, status)

        #cv2.imshow("test", imout)
#
        retval, buf = cv2.imencode('.jpg', imout)
        b64out = base64.b64encode(buf)
        payload = {}
        payload['b64'] = b64out.decode('utf-8')
        payload['res'] = res
        payload['status'] = status
        print(payload)
        emit('response', payload)


    except Exception as e:
        print(e)


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000)
    #app.run()
