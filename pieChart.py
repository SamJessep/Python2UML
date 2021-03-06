import matplotlib.pyplot as plt


class Pie:
    def __init__(self, labels, data, title):
        self.labels = labels
        self.data = data
        self.title = title

    def make_pie(self, out_path, name):
        fig1, ax1 = plt.subplots()
        ax1.pie(self.data, labels=self.labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(self.title)
        plt.savefig(f"{out_path}/{name}.png")
