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
        self.NIGHT = "21:00"
        self.showVideo =True

        self.record_video=False
        self.video_input = "rtsp://192.168.0.32:554/11"
        self.video_output = ".avi"
        self.img_output = ".jpg"
        self.ti = 0
        self.vs = None
        self.resize_frame = None
        

    def take_picture(self):

        try:
            #print("[INFO] opening streaming...", self.video_input)
            self.vs = cv2.VideoCapture(self.video_input)


            # if the frame dimensions are empty, set them
            #if self.W is None or self.H is None:
                #ret, frame = self.vs.read()
                #(self.H, self.W) = frame.shape[:2]


            # VideoCapture or VideoStream
            ret, frame = self.vs.read()
            if ret == False:
                print("[WARNING] Frame is empty")
            else:

                # ct stores current time
                ct = datetime.datetime.now()

                # ts store timestamp of current time
                ts = int(ct.timestamp())

                # Filename
                filename = str(ts) + '.jpg'


                self.resize_frame = cv2.resize(frame, (self.W, self.H))

                #cv2.rectangle(resize_frame,(2,2),(160,40),(62,84,61),cv2.FILLED)
                #cv2.putText(resize_frame, 'Day 01', (20, 30), font, 1, (180, 180, 180), 2,cv2.LINE_AA)


                path = self.directory + datetime.date.today().strftime("%Y%m%d")
                if not (os.path.isdir(path)):
                    os.makedirs(path)

                cv2.imwrite(path + FORMAT_DIR + filename, self.resize_frame)

                onlyfiles = next(os.walk(path))[2] #dir is your directory path as string
                print("Capture",len(onlyfiles),": ",ct.strftime("%Y-%m-%d %H:%M"))

                # show the output frame
                if self.showVideo:
                    cv2.imshow(self.WINDOW_NAME, self.resize_frame) #Muestra el vídeo

        except cv2.error as e:
            print("[ERROR] Problem reading")


        self.vs.release()



    def recordVideo(self):

        writer = None
        while self.record_video:
            if (writer == None):
                print("[INFO] opening streaming...", self.video_input)
                vs = cv2.VideoCapture(self.video_input)


                # if the frame dimensions are empty, set them
                if self.W is None or self.H is None:
                    frame = vs.read()
                    (self.H, self.W) = frame.shape[:2]

                ct = datetime.datetime.now()
                ts = int(ct.timestamp())


                path = self.directory + datetime.date.today().strftime("%Y%m%d") + FORMAT_DIR + str(ts)+ self.video_output
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(path , fourcc, 30,(self.W,self.H), True)
                print("Video start timestamp:-", ts)

            # VideoCapture or VideoStream
            frame = vs.read()
            resize_frame = cv2.resize(frame[1], (self.W, self.H))
            writer.write(resize_frame)
            cv2.imshow(self.WINDOW_NAME, resize_frame) #Muestra el vídeo
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("r"):
                self.record_video = not self.record_video

        if not self.record_video:
            if writer is not None:
                ct = datetime.datetime.now()
                ts = int(ct.timestamp())
                print("Video finish timestamp:-", ts)
                writer.release()
                writer = None
