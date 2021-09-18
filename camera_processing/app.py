#/usr/bin/env python3
from Snapshot import Snapshot
from flask import Flask, render_template, Response, request, url_for
import rospy
import time
from handle_camera import Camera
from vnbots_gazebo.srv import EndPosition

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

camera = Camera()

snapshot_image = Snapshot()

# Ignore this part, this for clear the cache
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/', methods=["GET", "POST"])
def index():
    """Video streaming home page."""
    if request.method == "POST":
        if request.form.get('Send') == 'SendLocation':
            # Get object and cotainer info from snapshot
            selectedObject = request.form.get('object')
            selectedContainer = request.form.get('container')
            endEffectorPosition = snapshot_image.getPosition(selectedObject,selectedContainer)
            if endEffectorPosition: 
                try:
                    xStart = endEffectorPosition[0]
                    yStart = endEffectorPosition[1]
                    zStart = endEffectorPosition[2]
                    container = endEffectorPosition[3]
                    # Send data to robot
                    rospy.ServiceProxy('MoveRobot', EndPosition)(xStart,yStart,zStart,container)
                except rospy.ServiceException as e:
                    pass
        
        # Create delay for take snapshot and save image
        Camera.snapshot = True
        time.sleep(0.3)
        Camera.snapshot = False
        time.sleep(0.3)
        snapshot_image.detectObject()
        time.sleep(0.3)
        return render_template("dropdown.html", objects=snapshot_image.listObject(), containers=['Container 1','Container 2'])

    return render_template('index.html')


def gen():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
