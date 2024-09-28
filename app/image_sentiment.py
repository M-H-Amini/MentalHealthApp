import random
from emotions import Emotions

class ImageSentiment:
    def __init__(self):
        self.emotions = Emotions()

    def analyze(self, img):
        dominant_emotion, emotions = self.emotions.predict(img)
        return dominant_emotion.capitalize()
