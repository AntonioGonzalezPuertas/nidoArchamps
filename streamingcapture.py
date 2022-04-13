import os
import cv2
import datetime


if os.name == 'nt':
    FORMAT_DIR = '\\' # Windows
else:
    FORMAT_DIR = '/' # Linux



#os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

class SC():
    def __init__(self):

        self.directory = os.path.dirname(os.path.abspath(__file__)) + FORMAT_DIR + r'output' + FORMAT_DIR
        
        self.WINDOW_NAME = 'Cameras'
        self.W = 1280
        self.H = 720
        self.TIME_LAPSE = 60
        self.TIME_LAPSE_DAY_MINUTES = 1
        self.TIME_LAPSE_NIGHT_HOURS = 1
        self.MORNING = "06:00"
        self.NIGHT = "22:00"
        self.showVideo =False

        self.record_video=False
        self.screenShot = False
        self.video_input = "rtsp://192.168.0.32:554/11"
        self.video_output = ".avi"
        self.img_output = ".jpg"
        self.ti = 0
        self.vs = None
        self.resize_frame = None
        print("[INFO] Streaming source:", self.video_input)
        
    def filename(self):
        # ct stores current time
        ct = datetime.datetime.now()

        # ts store timestamp of current time
        ts = int(ct.timestamp())

        # Filename
        return str(ts) + '.jpg'

    def path(self):
        path = self.directory + datetime.date.today().strftime("%Y%m%d")
        if not (os.path.isdir(path)):
            os.makedirs(path)

        return path


    def take_picture(self):

        try:
            if not self.showVideo and not self.record_video:
                self.vs = cv2.VideoCapture(self.video_input)

            # VideoCapture or VideoStream
            ret, frame = self.vs.read()
            if ret == False:
                print("[WARNING] Frame is empty")
            else:


                self.resize_frame = cv2.resize(frame, (self.W, self.H))

                filename = self.filename()
                path = self.path()

                cv2.imwrite(path + FORMAT_DIR + filename, self.resize_frame)

                onlyfiles = next(os.walk(path))[2] #dir is your directory path as string
                print("[INFO] Capture",len(onlyfiles),": ",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), filename)

                # show the output frame
                if not self.showVideo:
                    cv2.imshow(self.WINDOW_NAME, self.resize_frame) #Muestra el vídeo

        except cv2.error as e:
            print("[ERROR] Problem reading")

        if not (self.showVideo or self.record_video):
            self.vs.release()
            self.vs =None



    def liveVideo(self):

        try:
            self.showVideo=True
            print("[INFO] Start streaming")

            self.vs = cv2.VideoCapture(self.video_input)
            while self.showVideo:

                # VideoCapture or VideoStream
                ret, frame = self.vs.read()
                if ret == False:
                    print("[WARNING] Frame is empty")
                else:
                    resize_frame = cv2.resize(frame, (self.W, self.H))
                    cv2.imshow(self.WINDOW_NAME, resize_frame) #Muestra el vídeo

                key = cv2.waitKey(1) & 0xFF

                if key == ord("r"):
                    self.showVideo=False
                    self.record_video=True
                if key == ord("p"):
                    self.take_picture()
                if key == ord("v"):
                    self.showVideo = False
            self.vs.release()
            self.vs =None
            print("[INFO] Stop streaming")

        except cv2.error as e:
            print("[ERROR] Problem streaming video")
            if self.vs != None:
                self.vs.release()
                self.vs =None
                print("[INFO] Closing stream")

        if self.record_video:
            self.recordVideo()



    def recordVideo(self):

        try:
            writer = None
            self.record_video=True
            while self.record_video:
                if (writer == None):
                    self.vs = cv2.VideoCapture(self.video_input)


                    # if the frame dimensions are empty, set them
                    if self.W is None or self.H is None:
                        frame = self.vs.read()
                        (self.H, self.W) = frame.shape[:2]

                    ct = datetime.datetime.now()
                    ts = int(ct.timestamp())


                    path = self.directory + datetime.date.today().strftime("%Y%m%d") + FORMAT_DIR + str(ts)+ self.video_output
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    writer = cv2.VideoWriter(path , fourcc, 30,(self.W,self.H), True)
                    print("[INFO] Video start timestamp:-", ts)

                # VideoCapture or VideoStream
                frame = self.vs.read()
                resize_frame = cv2.resize(frame[1], (self.W, self.H))
                writer.write(resize_frame)
                cv2.imshow(self.WINDOW_NAME, resize_frame) #Muestra el vídeo
                key = cv2.waitKey(1) & 0xFF

                if key == ord("r"):
                    self.record_video = False

            if not self.record_video:
                if writer is not None:
                    ct = datetime.datetime.now()
                    ts = int(ct.timestamp())
                    print("[INFO] Video finish timestamp:-", ts)
                    writer.release()
        except cv2.error as e:
            print("[ERROR] Problem recording streaming video")
            if self.vs != None:
                self.vs.release()
                self.vs =None
                print("[INFO] Closing stream")
