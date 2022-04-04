
import argparse
import time
import cv2
import datetime
import myScheduler
import schedule
import streamingcapture


#by default

mySC = streamingcapture.SC()
myScheduler = myScheduler.Scheduler(mySC)

def loop():
    # loop over frames from the video stream

    print("Running Scheduler. TimeLapse:",str(mySC.TIME_LAPSE) + 'sec')
    print("Between:", str(mySC.MORNING) + 'h' ,"and", str(mySC.NIGHT) + 'h')

    print("Picture taken")
    mySC.take_picture()

    while True:
        schedule.run_pending()

        if mySC.record_video:
            mySC.recordVideo()

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        if key == ord("r"):
            mySC.record_video = not mySC.record_video
        if key == ord("s"):
            mySC.showVideo = not mySC.showVideo

        if key == ord("0"):
            mySC.TIME_LAPSE = 5
        if key == ord("1"):
            mySC.TIME_LAPSE = 60
        if key == ord("2"):
            mySC.TIME_LAPSE = 120




def main():

    loop()

    # close any open windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
