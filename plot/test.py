import matplotlib.pyplot as plt

def plot_categories():
    names = ['automobile', 'airplane', 'truck', 'ship']
    values = [20, 69, 10, 100]

    plt.bar(names, values)
    plt.suptitle('Categorical Plotting')
    plt.show()

def plot_sentiments():
    print("p/n")

if __name__ == '__main__':
    plot_sentiments()