import time
import io
import threading
import picamera
import cv2
import numpy as np
import numpy as np
import argparse
import imutils

from collections import deque
from imutils.video import VideoStream


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    cam = None
    nbPic = 0

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame.tobytes()

    def save_frame(self):
        if self.cam == None:
            print("No camera")
        else:
            self.cam.capture('./pictures/image'+str(self.nbPic)+'.png')
            self.nbPic += 1

    @classmethod
    def _thread(cls):
        #with picamera.PiCamera() as camera:
        #with cv2.VideoCapture(1) as camera:
       
        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=0,help="max buffer size")
        args = vars(ap.parse_args())

        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the list of tracked points
        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)
        pts = deque(maxlen=args["buffer"])


        camera = cv2.VideoCapture(0)
        Camera.cam = camera
            # camera setup
            #camera.resolution = (854, 480)
            #camera.hflip = True
            #camera.vflip = True
        camera.set(3, 640)
        camera.set(4, 480) 

            # let camera warm up
            #camera.start_preview()
            #time.sleep(2)

       # stream = io.BytesIO()
            #for foo in camera.capture_continuous(stream, 'jpeg',
            #                                     use_video_port=True):
        res, frame = camera.read()
   
        while res:

            res, frame = camera.read()
 
            # resize the frame, blur it, and convert it to the HSV color space
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

 
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small blobs left in the mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
 
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
            # update the points queue
            pts.appendleft(center)

            # loop over the set of tracked points
            for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore them
                if pts[i - 1] is None or pts[i] is None:
                        continue
 
                # otherwise, compute the thickness of the line and draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)


            ret, cls.frame = cv2.imencode('.jpg',frame)

            # store frame
            #stream.seek(0)
            #str_frame =  cv2.imencode('.jpeg', frame)[1].tostring()
            #cls.frame = stream.read()

            # reset stream for next frame
            #stream.seek(0)
            #stream.truncate()

            #nparr = np.fromstring(str_frame, np.uint8)
            #cls.frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds stop the thread
            if time.time() - cls.last_access > 10:
                break
        cls.thread = None
