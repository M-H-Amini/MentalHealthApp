import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud

class Visualizer:
    def __init__(self):
        pass

    def generate_sentiment_graph(self, sentiment_data):
        if not sentiment_data:
            sentiments = []
            timestamps = []
        else:
            timestamps = [data[0] for data in sentiment_data]
            sentiments = [self.sentiment_to_numeric(data[1]) for data in sentiment_data]
        
        plt.figure()
        plt.plot(timestamps, sentiments, marker='o')
        plt.title('Sentiment Trends')
        plt.xlabel('Timestamp')
        plt.ylabel('Sentiment Level')
        plt.yticks([0, 1, 2], ['Sad', 'Neutral', 'Happy'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.savefig('static/images/sentiment_graph.png')
        plt.close()

    def generate_attention_graph(self, attention_data):
        if not attention_data:
            attentions = []
            timestamps = []
        else:
            timestamps = [data[0] for data in attention_data]
            attentions = [self.attention_to_numeric(data[1]) for data in attention_data]

        plt.figure()
        plt.plot(timestamps, attentions, marker='o', color='orange')
        plt.title('Attention Trends')
        plt.xlabel('Timestamp')
        plt.ylabel('Attention Level')
        plt.yticks([0, 1], ['Distracted', 'Focused'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.savefig('static/images/attention_graph.png')
        plt.close()

    def generate_word_cloud(self, text):
        if not text.strip():
            text = "No data available"

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        plt.figure(figsize=(15, 7.5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('static/images/word_cloud.png')
        plt.close()

    @staticmethod
    def sentiment_to_numeric(sentiment):
        mapping = {'Sad': 0, 'Neutral': 1, 'Happy': 2}
        return mapping.get(sentiment, 1)

    @staticmethod
    def attention_to_numeric(attention):
        mapping = {'Distracted': 0, 'Focused': 1}
        return mapping.get(attention, 0)
