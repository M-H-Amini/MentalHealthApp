import random
import matplotlib.pyplot as plt
import os

class Visualizer:
    def __init__(self):
        pass

    def visualizePlot(self):
        # Code to get sentiment from image
        plt.figure()
        plt.plot([1, 2, 3, 4], random.sample(range(1, 10), 4))
        plt.savefig(os.path.join("data", "plot.png"))
        plt.close()
    
    def visualizeWords(self):
        # Code to get sentiment from image
        plt.figure()
        plt.plot([1, 2, 3, 4], random.sample(range(1, 10), 4))
        plt.savefig(os.path.join("data", "cloud.png"))
        plt.close()