from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

import analyser_ui
from src import database, RabbitMq

class RabbitMqThread(QtCore.QThread):
    def __init__(self, user_data, listWidget, funCallUpdate, parent=None):
        super(RabbitMqThread, self).__init__(parent)
        self.rabbitmq = RabbitMq.RabbitMq(user_data, listWidget, funCallUpdate)

    def run(self):
        while True:
            self.rabbitmq.receive_message()


class AlphaViewAppUI(QtWidgets.QMainWindow, analyser_ui.Ui_QMainWindow):

    def __init__(self, parent=None):
        super(AlphaViewAppUI, self).__init__(parent)
        self.setupUi(self)

        self.user_data = {}
        self.rmq = RabbitMqThread(self.user_data, self.listWidget, self.update_user_state)
        self.start_mqthread()

        # init image classifier graph
        self.figure_imgcls = Figure()
        self.canvas_imgcls = FigureCanvasQTAgg(self.figure_imgcls)
        self.axis_imgcls = self.figure_imgcls.add_subplot(111)
        self.axis_imgcls.set(title="Image classifier", xlabel="classes", ylabel="# images")

        # init mood text graph
        self.figure_mood = Figure()
        self.canvas_mood = FigureCanvasQTAgg(self.figure_mood)
        self.axis_mood = self.figure_mood.add_subplot(111)
        self.axis_mood.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.axis_mood.set(title="Sentiments analyser from text", xlabel="# Messages", ylabel="Mood")
        self.classes = ['airplane', 'automobile', 'ship', 'truck']

        self.plot_classifier_images_graph([0])
        self.plot_text_mood_graph([0])

        self.verticalLayoutText.addWidget(self.canvas_mood)
        self.verticalLayoutImages.addWidget(self.canvas_imgcls)

        self.listWidget.currentItemChanged.connect(self.update_user_state)

    def start_mqthread(self):
        if not self.rmq.isRunning():
            self.rmq.start()

    def init_users(self):
        users = self.mydb.get_users()
        for user in users:
            self.listWidget.addItem(user)

    def update_user_state(self):
        # self.plot_text_mood_graph()
        try:
            username = self.listWidget.currentItem().text()
            print(f"Ai dat click pe {username}")
            text_data = self.user_data[username]["text"]
            img_cl_data = list(self.user_data[username]["images"].values())

            self.plot_classifier_images_graph(img_cl_data)
            self.plot_text_mood_graph(text_data)
        except:
            pass


    def plot_classifier_images_graph(self, values):
        self.axis_imgcls.clear()
        self.axis_imgcls.bar(self.classes, values)
        self.canvas_imgcls.draw()

    def plot_text_mood_graph(self, values):
        self.axis_mood.clear()
        n = len(values) + 1
        x = range(1, n)
        self.axis_mood.axhline(0, 0, n, color ='green')
        self.axis_mood.plot(x, values)
        self.axis_mood.set_ylim(-1, 1)
        self.canvas_mood.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AlphaViewAppUI()
    form.show()
    app.exec_()