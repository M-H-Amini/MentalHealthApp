import random
from gaze import GazeDetector
import cv2

class ImageAttention:
    def __init__(self):
        self.gaze = GazeDetector()

    def analyze(self, image):
        if isinstance(image, str):
            image = cv2.imread(image)
        attention_states = ['Distracted', 'Focused']
        result = self.gaze.isFocused(image)
        return attention_states[int(result)]
