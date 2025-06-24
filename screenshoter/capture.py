#import numpy as np
#from numba import jit
from numpy import frombuffer, ascontiguousarray
import win32gui, win32ui, win32con
# Set DPI Awareness  (Windows 10 and 8)
# https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)



class Capture:

    # State of the class
    hwnd = None
    # Get Screen Size
    w = int(ctypes.windll.user32.GetSystemMetrics(0) * 3/5)
    h = int(ctypes.windll.user32.GetSystemMetrics(1) * 3/5)
    print((ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)))
    print((w, h))

    # Receive Window Property
    #def __init__(self, window_name):
    #    self.hwnd = win32gui.FindWindow(None, window_name)
    

    # Get image data with some Windows API shit
    # https://learn.microsoft.com/en-us/windows/win32/gdi/capturing-an-image
    def get_screenshot(self):

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # UpperLeft Draw Position (X,Y),  Amount of Pixels to capture (W,H),  Bitmap file,  UpperLeft Pixel crop (X,Y),  win32con.THING
        # Draw Position is the pixel to offset the capture by. This is NOT a crop.
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (int(self.w / 3), int(self.h / 3)), win32con.SRCCOPY)

        # Save data as img variable
        img = frombuffer(dataBitMap.GetBitmapBits(True), dtype='uint8')
        img.shape = (self.h, self.w, 4)
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        # Garbage Collect
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Remove Alpha channel and process the image or something
        img = img[...,:3]
        img = ascontiguousarray(img)

        return img