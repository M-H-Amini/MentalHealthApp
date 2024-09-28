import random

class ImageSentiment:
    def __init__(self):
        pass

    def get_sentiment(self, image):
        # Code to get sentiment from image
        sentiments = ["Happy", "Sad", "Angry", "Neutral"]
        return random.choice(sentiments)