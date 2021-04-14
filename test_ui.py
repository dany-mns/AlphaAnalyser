from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

import analyser_ui
from src import database


class AlphaViewAppUI(QtWidgets.QMainWindow, analyser_ui.Ui_QMainWindow):

    def __init__(self, parent=None):
        super(AlphaViewAppUI, self).__init__(parent)
        self.mydb = database.Database("admin", "password", "aVoice")
        self.setupUi(self)
        self.init_users()
        self.init_text_mood_gp()
        self.init_img_cls_gp()

        # plot images
        self.plot_classifier_images_graph()
        self.plot_text_mood_graph()

        # plot text sentiments
        self.verticalLayoutText.addWidget(self.canvas2)
        self.verticalLayoutImages.addWidget(self.canvas)


        self.listWidget.currentItemChanged.connect(self.ViewUserState)

    def init_users(self):
        users = self.mydb.get_users()
        for user in users:
            self.listWidget.addItem(user)

    def ViewUserState(self):
        # self.plot_text_mood_graph()
        self.plot_classifier_images_graph()
        self.plot_text_mood_graph()

    def init_img_cls_gp(self):
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.bg = self.figure.canvas.copy_from_bbox(self.axis.bbox)

    def init_text_mood_gp(self):
        self.figure2 = Figure()
        self.canvas2 = FigureCanvasQTAgg(self.figure2)
        self.axis2 = self.figure2.add_subplot(111)
        self.axis2.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.axis2.set(title="Sentiments analyser from text", xlabel="# Messages", ylabel="Mood")

    def plot_classifier_images_graph(self):
        self.axis.clear()

        names = ['automobile', 'airplane', 'truck', 'ship']
        values = np.random.randint(0, 300, 4)
        self.axis.bar(names, values)
        self.axis.set(title="Image classifier", xlabel="classes", ylabel="# images")

        self.canvas.draw()

    def plot_text_mood_graph(self):
        self.axis2.clear()

        x = range(1, 21)
        y = np.random.randint(-1, 2, 20)
        y_mean = []
        for i, elem in enumerate(y):
            y_mean.append(np.mean(y[:(i+1)]))
        self.axis2.axhline(0, 0, 20, color ='green')
        self.axis2.plot(x, y_mean)
        self.axis2.set_ylim(-1, 1)

        self.canvas2.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AlphaViewAppUI()
    form.show()
    app.exec_()