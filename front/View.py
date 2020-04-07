import sys

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWidgets import QApplication

from front.Bridge import Bridge


class View:

    def __init__(self):
        self.__bridge = None

    def start_app(self):
        app = QApplication(sys.argv)

        self.__bridge = Bridge("example.txt")
        self.__bridge.rootContext().setContextProperty("bridge", self.__bridge)
        self.__bridge.setSource(QUrl('front/qmls/view.qml'))

        self.__bridge.show()

        app.exec_()
        del self.__bridge
        sys.exit()