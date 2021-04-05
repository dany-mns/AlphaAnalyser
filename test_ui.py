from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

import analyser_ui

class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)
        names = ['automobile', 'airplane', 'truck', 'ship']
        values = [20, 69, 10, 100]

        self.axis.bar(names, values)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)#QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)

class ThreadSample(QtCore.QThread):
    newSample = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadSample, self).__init__(parent)

    def run(self):
        randomSample = np.random.sample(range(0, 10), 10)

        self.newSample.emit(randomSample)


class TestAppUI(QtWidgets.QMainWindow, analyser_ui.Ui_QMainWindow):
    def __init__(self, parent=None):
        super(TestAppUI, self).__init__(parent)
        self.setupUi(self)

        self.listWidget.addItem("Ana")
        self.listWidget.insertItem(1, "Bob")

        # plot images
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        names = ['automobile', 'airplane', 'truck', 'ship']
        values = [20, 69, 10, 100]
        self.axis.bar(names, values)
        self.verticalLayoutImages.addWidget(self.canvas)

        # plot text sentiments
        x = range(1, 21)
        y = np.random.randint(-1, 2, 20)
        y_mean = []
        print(y)
        for i, elem in enumerate(y):
            y_mean.append(np.mean(y[:(i+1)]))
        print(y_mean)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvasQTAgg(self.figure2)
        self.axis2 = self.figure2.add_subplot(111)
        self.axis2.set_ylim(-1, 1)
        self.axis2.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.axis2.set(title="Sentiments analyser from text", xlabel="# Messages", ylabel="Mood")
        self.axis2.axhline(0, 0, 20, color ='green')

        # self.axis2.set_xticks(range(0, 20))
        self.axis2.plot(x, y_mean)
        self.verticalLayoutText.addWidget(self.canvas2)

        self.listWidget.currentItemChanged.connect(self.PrintClick)

    def PrintClick(self):
        print(self.listWidget.currentItem().text())

def main():
    app = QApplication(sys.argv)
    form = TestAppUI()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()