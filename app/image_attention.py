import random

class ImageAttention:
    def __init__(self, image):
        self.image = image

    def analyze(self):
        attention_states = ['Focused', 'Distracted']
        result = random.choice(attention_states)
        return result
