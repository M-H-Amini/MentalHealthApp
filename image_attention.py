import random

class ImageAttention:
    def __init__(self, image_path):
        self.image_path = image_path

    def get_attention(self):
        # Code to get sentiment from image
        sentiments = ["Distracted", "Focused"]
        return random.choice(sentiments)