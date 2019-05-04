import time
import io
import threading
import picamera
import cv2
import numpy as np


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
        camera = cv2.VideoCapture(1)
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
