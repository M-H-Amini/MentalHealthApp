import random

class ImageSentiment:
    def __init__(self, image_path):
        self.image_path = image_path

    def get_sentiment(self):
        # Code to get sentiment from image
        sentiments = ["Happy", "Sad", "Angry", "Neutral"]
        return random.choice(sentiments)