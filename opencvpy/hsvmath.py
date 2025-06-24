import numpy as np



class hsvMathClass:

    # State of the class
    hsvcolor = (360, 100, 100)
    ColorThreshold = 0.5


    # Receieve Color and Threshold Property 
    def __init__(self, hsvcolor=(360, 100, 100), ColorThreshold=0.5):
        self.hsvcolor = hsvcolor
        self.ColorThreshold = ColorThreshold



    # GIMP format: (360, 100%, 100%)  ->  OpenCV format: (180, 255, 255)
    def hsv_lowerBound(self):
        ColorGIMP = np.array(self.hsvcolor)
        ColorOCV = np.array([int(ColorGIMP[0] / 2), int(ColorGIMP[1] * 2.555), int(ColorGIMP[2] * 2.555)])
        ThresholdArray = np.array([int(ColorOCV[0] * self.ColorThreshold), int(ColorOCV[1] * self.ColorThreshold), int(ColorOCV[2] * self.ColorThreshold)])

        lowerBound = np.array([
            max(min((ColorOCV[0] - ThresholdArray[0]), 180), 0),
            max(min((ColorOCV[1] - ThresholdArray[1]), 255), 0),
            max(min((ColorOCV[2] - ThresholdArray[2]), 255), 0)
        ])
        return lowerBound



    # GIMP format: (360, 100%, 100%)  ->  OpenCV format: (180, 255, 255)
    def hsv_upperBound(self):
        ColorGIMP = np.array(self.hsvcolor)
        ColorOCV = np.array([int(ColorGIMP[0] / 2), int(ColorGIMP[1] * 2.555), int(ColorGIMP[2] * 2.555)])
        ThresholdArray = np.array([int(ColorOCV[0] * self.ColorThreshold), int(ColorOCV[1] * self.ColorThreshold), int(ColorOCV[2] * self.ColorThreshold)])

        upperBound = np.array([
            max(min((ColorOCV[0] + ThresholdArray[0]), 180), 0),
            max(min((ColorOCV[1] + ThresholdArray[1]), 255), 0),
            max(min((ColorOCV[2] + ThresholdArray[2]), 255), 0)
        ])
        return upperBound