import cv2
from win32gui import FindWindow, GetForegroundWindow, GetWindowText, SetForegroundWindow
from time import time
from capture import Capture
from processing import ImageProcessing
from keyboard import is_pressed



captureClass = Capture()
processingClass = ImageProcessing((358, 88, 93), 0.2)
lowerBound = processingClass.hsv_lowerBound()
upperBound = processingClass.hsv_upperBound()
#(GetWindowText(GetForegroundWindow()) == "Desktop")

while (FindWindow(None, "Desktop") != 0):
    loop_time = time()

    # Infinite Loop
    while (True):
        loop_time = time()
        
        # Capture Screen
        screenshot = captureClass.get_screenshot()
        #screenshot = cv2.resize(screenshot, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)

        # Apply HSV Filter and Mask
        hsvScreenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        hsvMask = cv2.inRange(hsvScreenshot, lowerBound, upperBound)

        # Find Contours
        hsvMaskResult, hulledContours = processingClass.draw_contours(screenshot, hsvScreenshot, hsvMask)

        # Get center points from Contours
        contourCenters = processingClass.get_centers(hulledContours)
        # Aim
        if (is_pressed('q')):
            hsvMaskResult, scaledCenters = processingClass.aim_to_contours(contourCenters, hsvMaskResult, True)


        # Show final Results
        cv2.imshow("Final Result", hsvMaskResult)
        #cv2.imshow("Raw Screenshot", screenshot)
        #cv2.imshow("Image Mask", hsvMask)


        keypressed = cv2.waitKey(1)
        # FPS Counter
        if keypressed == ord("f"):
            # Im adding a very small number to prevent dividing by zero
            print("FPS: {}".format(1 / ((time() - loop_time) + 0.00001)))
        # Exit key
        if  keypressed == ord("`"):
            exit()
        
    cv2.destroyAllWindows()
print("kill urself")