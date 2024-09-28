import random

class ImageSentiment:
    def __init__(self, image):
        self.image = image

    def analyze(self):
        sentiments = ['Happy', 'Sad', 'Neutral']
        result = random.choice(sentiments)
        return result
