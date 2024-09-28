import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

class Visualizer:
    def __init__(self):
        # Set Seaborn style for better aesthetics
        sns.set(style="whitegrid")

    def generate_sentiment_graph(self, sentiment_data):
        if not sentiment_data:
            sentiments = []
            timestamps = []
        else:
            timestamps = [data[0] for data in sentiment_data]
            sentiments = [self.sentiment_to_numeric(data[1]) for data in sentiment_data]
        
        # Prepare data for pie chart
        sentiment_counts = {0: 0, 1: 0, 2: 0}
        for sentiment in sentiments:
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
            else:
                sentiment_counts[sentiment] = 1

        labels = ['Sad', 'Neutral', 'Happy']
        sizes = [sentiment_counts.get(0, 0), sentiment_counts.get(1, 0), sentiment_counts.get(2, 0)]
        colors = sns.color_palette("pastel")[0:3]

        # Create subplots: 1 row, 2 columns
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))

        # Left Subplot: Line Plot
        sns.lineplot(x=timestamps, y=sentiments, marker='o', ax=axes[0], palette="viridis")
        axes[0].set_title('Sentiment Trends', fontsize=16)
        axes[0].set_xlabel('Timestamp', fontsize=14)
        axes[0].set_ylabel('Sentiment Level', fontsize=14)
        axes[0].set_yticks([0, 1, 2])
        axes[0].set_yticklabels(['Sad', 'Neutral', 'Happy'])
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True)

        # Right Subplot: Pie Chart
        axes[1].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        axes[1].set_title('Sentiment Distribution', fontsize=16)
        axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.tight_layout()
        plt.savefig('static/images/sentiment_graph.png')
        plt.close()

    def generate_attention_graph(self, attention_data):
        if not attention_data:
            attentions = []
            timestamps = []
        else:
            timestamps = [data[0] for data in attention_data]
            attentions = [self.attention_to_numeric(data[1]) for data in attention_data]
        
        # Prepare data for pie chart
        attention_counts = {0: 0, 1: 0}
        for attention in attentions:
            if attention in attention_counts:
                attention_counts[attention] += 1
            else:
                attention_counts[attention] = 1

        labels = ['Distracted', 'Focused']
        sizes = [attention_counts.get(0, 0), attention_counts.get(1, 0)]
        colors = sns.color_palette("Oranges")[0:2]

        # Create subplots: 1 row, 2 columns
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))

        # Left Subplot: Line Plot
        sns.lineplot(x=timestamps, y=attentions, marker='o', ax=axes[0], color='orange')
        axes[0].set_title('Attention Trends', fontsize=16)
        axes[0].set_xlabel('Timestamp', fontsize=14)
        axes[0].set_ylabel('Attention Level', fontsize=14)
        axes[0].set_yticks([0, 1])
        axes[0].set_yticklabels(['Distracted', 'Focused'])
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True)

        # Right Subplot: Pie Chart
        axes[1].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        axes[1].set_title('Attention Distribution', fontsize=16)
        axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.tight_layout()
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
