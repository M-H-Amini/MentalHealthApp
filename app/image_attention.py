import random
from gaze import GazeDetector

class ImageAttention:
    def __init__(self, image):
        self.gaze = GazeDetector()
        self.image = image


    def analyze(self, image):
        attention_states = ['Focused', 'Distracted']
        result = random.choice(attention_states)
        return result
