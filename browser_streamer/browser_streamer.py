from flask import Flask, Response, render_template
import numpy as np
import cv2
import threading


class BrowserStreamer:
    def __init__(self, port : int = 5000):
        self.app = Flask(__name__)
        self.port = port
        self.frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)
        self.video_feed_thread = threading.Thread(target=self.run)
        self.video_feed_thread.start()


    def run(self):
        @self.app.route('/video_feed')
        def video_feed():
            return Response(self._generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/')
        def index():
            return render_template('index.html')

        # Run Flask server
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

    def render(self, frame):
        self.frame = frame

    def _generate_video_feed(self):
        while True:
            # Capture frame from camera
            _, buffer = cv2.imencode('.jpg', self.frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            

if __name__ == '__main__':
    streamer = BrowserStreamer()
    streamer.render(255 * np.ones((480, 640, 3), dtype=np.uint8))