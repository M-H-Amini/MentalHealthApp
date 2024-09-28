import random

class Goal:
    def get_motivation(self):
        quotes = [
            "Believe you can and you're halfway there.",
            "Your limitation—it’s only your imagination.",
            "Push yourself, because no one else is going to do it for you."
        ]
        images = [
            "motivation1.jpg",
            "motivation2.jpg",
            "motivation3.jpg"
        ]
        quote = random.choice(quotes)
        image = random.choice(images)
        return quote, image
