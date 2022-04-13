
import cv2
import myScheduler
import schedule
import streamingcapture


#by default

mySC = streamingcapture.SC()
myScheduler = myScheduler.Scheduler(mySC)

def loop():
    # loop over frames from the video stream

    print("[INFO] Running Scheduler. TimeLapse:",str(mySC.TIME_LAPSE_DAY_MINUTES) + 'min')
    print("[INFO] Between:", str(mySC.MORNING)  ,"and", str(mySC.NIGHT) + 'h')

    mySC.take_picture()

    while True:
        schedule.run_pending()

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        if key == ord("r"):
            mySC.recordVideo()
        if key == ord("p"):
            mySC.take_picture()
        if key == ord("v"):
            mySC.liveVideo()
        if key == ord("d"):
            myScheduler.startDay()
        if key == ord("n"):
            myScheduler.endDay()

        if key == ord("0"):
            myScheduler.changeSchedule(999)
        if key == ord("1"):
            myScheduler.changeSchedule(1)
        if key == ord("2"):
            myScheduler.changeSchedule_sec(5)
        if key == ord("3"):
            myScheduler.changeSchedule_sec(10)
        if key == ord("4"):
            myScheduler.changeSchedule_sec(30)

def click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        mySC.recordVideo()
    elif event == cv2.EVENT_LBUTTONUP:
        mySC.record_video = False



def main():
    cv2.namedWindow(mySC.WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowTitle(mySC.WINDOW_NAME, mySC.WINDOW_NAME)
    if mySC.W and mySC.H:
    	cv2.resizeWindow(mySC.WINDOW_NAME, mySC.W, mySC.H)

    cv2.setMouseCallback(mySC.WINDOW_NAME,click_event)
	
    loop()
    
    
    

    # close any open windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
