import threading
import time
import gunicorn

import cv2
from flask import Flask, render_template, Response
from multiprocessing import Process
import threading
import time


app = Flask(__name__)
exit_event = False

def protocol():
    time.sleep(1)

    # OpenCV video capture
    video_capture = cv2.VideoCapture(1)


    def generate_frames():
        while not exit_event:
            # Capture video frame-by-frame
            success, frame = video_capture.read()
            # time.sleep(5)

            if not success:
                break

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


    @app.route('/')
    def index():
        # Render the HTML template
        return render_template('index2.html')


    @app.route('/video_feed')
    def video_feed():
        # Return the video stream response
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run(host='0.0.0.0')


def stop():
    global exit_event
    print('here')
    time.sleep(15)
    print('here 2')
    exit_event = True


t = threading.Thread(target=protocol())
t.run()
stop()
