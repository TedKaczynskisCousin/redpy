import os
import cv2
from time import time
from capture import Capture
from keyboard import is_pressed
#import numba

os.chdir(os.path.dirname(os.path.abspath(__file__)))

captureClass = Capture()
loop_time = time()

# Infinite Loop
while (True):
    loop_time = time()
    
    # Get Screen
    screenshot = captureClass.get_screenshot()

    # Show final Result
    cv2.imshow("Matches", screenshot)

    keypressed = cv2.waitKey(1)    
    # FPS Counter
    if keypressed == ord("f"):
        # Im adding a very small number to prevent dividing by zero
        print("FPS: {}".format(1 / ((time() - loop_time) + 0.00001)))
    # Exit key
    if  keypressed == ord("`"):
        break
    
    if (is_pressed('e')):
        print('positives/{}.png'.format(loop_time))
        cv2.imwrite('positives/{}.png'.format(loop_time), captureClass.get_screenshot())
    if (is_pressed('q')):
        print('negatives/{}.png'.format(loop_time))
        cv2.imwrite('negatives/{}.png'.format(loop_time), captureClass.get_screenshot())
   
cv2.destroyAllWindows()
