import cv2
import pyautogui
from numpy import array
import ctypes


class ImageProcessing:

    # State of the class
    hsvcolor = (360, 100, 100)
    ColorThreshold = 0.5
    # Get Offset Size
    screenW = int(ctypes.windll.user32.GetSystemMetrics(0) / 5)
    screenH = int(ctypes.windll.user32.GetSystemMetrics(1) / 5)


    # Receieve Color and Threshold Property 
    def __init__(self, hsvcolor=(360, 100, 100), ColorThreshold=0.5):
        self.hsvcolor = hsvcolor
        self.ColorThreshold = ColorThreshold


    # Create HSV Mask, then find and draw Contours
    def draw_contours(self, screenshot, hsvFilter, hsvMask):
        hsvMaskResult = cv2.bitwise_and(screenshot, hsvFilter, mask= hsvMask)

        contours, hierarchy = cv2.findContours(hsvMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        hulledContours = []
        # For every contour...
        for i in range(len(contours)):
            # Approximate Contours using ConvexHull
            hulledContours.append(cv2.convexHull(contours[i], True))
            # Draw Convex Hull Contours and Fill
            cv2.drawContours(hsvMaskResult, hulledContours, -1, (0, 255, 0), cv2.FILLED)
        #print(hsvMaskResult[1][86])
        return hsvMaskResult, hulledContours



    # Find Points from Contours
    def get_centers(self, hulledContours):
        contourCenters = []
        # For every contour...
        for i in range(len(hulledContours)):
            # Get center points
            x,y,w,h = cv2.boundingRect(hulledContours[i])
            contourCenters.append((x + int(w/2), y + int(h/4))) # Apply Y Offset
        return contourCenters



    # Apply center point procedures
    def aim_to_contours(self, contourCenters, hsvMaskResult, drawPoints=False, aimto=True):
        # Draw Center Points and then convert them to screen format by reverting all scaling
        scaledCenters = []
        for p in range(len(contourCenters)):
            if (drawPoints):
                cv2.circle(hsvMaskResult, contourCenters[p], 4, (0, 0, 255), -1)
            #scaledCenters.append(( int((contourCenters[p][0] * (4/3)) + self.screenW), int((contourCenters[p][1] * (4/3) + self.screenH)) ))
            if (aimto):
                pyautogui.moveTo(int((contourCenters[p][0]) + self.screenW), int((contourCenters[p][1] + self.screenH)), 0, pyautogui.easeInQuad)
            #print((int((contourCenters[p][0] * (4/3)) + self.screenW), int((contourCenters[p][1] * (4/3) + self.screenH))))
        return hsvMaskResult, scaledCenters



    # GIMP format: (360, 100%, 100%)  ->  OpenCV format: (180, 255, 255)
    def hsv_lowerBound(self):
        ColorGIMP = array(self.hsvcolor)
        ColorOCV = array([int(ColorGIMP[0] / 2), int(ColorGIMP[1] * 2.555), int(ColorGIMP[2] * 2.555)])
        ThresholdArray = array([int(ColorOCV[0] * self.ColorThreshold), int(ColorOCV[1] * self.ColorThreshold), int(ColorOCV[2] * self.ColorThreshold)])

        lowerBound = array([
            max(min((ColorOCV[0] - ThresholdArray[0]), 180), 0),
            max(min((ColorOCV[1] - ThresholdArray[1]), 255), 0),
            max(min((ColorOCV[2] - ThresholdArray[2]), 255), 0)
        ])
        return lowerBound



    # GIMP format: (360, 100%, 100%)  ->  OpenCV format: (180, 255, 255)
    def hsv_upperBound(self):
        ColorGIMP = array(self.hsvcolor)
        ColorOCV = array([int(ColorGIMP[0] / 2), int(ColorGIMP[1] * 2.555), int(ColorGIMP[2] * 2.555)])
        ThresholdArray = array([int(ColorOCV[0] * self.ColorThreshold), int(ColorOCV[1] * self.ColorThreshold), int(ColorOCV[2] * self.ColorThreshold)])

        upperBound = array([
            max(min((ColorOCV[0] + ThresholdArray[0]), 180), 0),
            max(min((ColorOCV[1] + ThresholdArray[1]), 255), 0),
            max(min((ColorOCV[2] + ThresholdArray[2]), 255), 0)
        ])
        return upperBound
    
