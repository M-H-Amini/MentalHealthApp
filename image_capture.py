import random
import datetime

class ImageCapture:
    def __init__(self, folder):
        self.folder = folder

    def capture(self):
        ##  Code to capture image from webcam and save it
        ##  to the folder with the name as current timestamp
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        return filename

