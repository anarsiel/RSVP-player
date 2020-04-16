from PySide2.QtCore import Slot, Qt, QEvent
from PySide2.QtQuickWidgets import QQuickWidget

from body.Controller import Controller


class Bridge(QQuickWidget):
    def __init__(self):
        super().__init__()

        self.__controller = Controller()
        self.__key_to_id = { Qt.Key_Space : "space",
                             Qt.Key_Shift : "shift",
                             Qt.Key_Up    : "up",
                             Qt.Key_Down  : "down",
                             Qt.Key_Left  : "left",
                             Qt.Key_Right : "right" }
    #
    #   Slots
    #

    @Slot()
    def start(self):
        self.__start()

    @Slot()
    def stop(self):
        self.__stop()

    @Slot(result=str)
    def get_word_A(self):
        return self.__controller.get_splitted_word()[0]

    @Slot(result=str)
    def get_word_B(self):
        return self.__controller.get_splitted_word()[1]

    @Slot(result=str)
    def get_word_C(self):
        return self.__controller.get_splitted_word()[2]

    @Slot(result=str)
    def get_wpm(self):
        return str(self.__controller.get_wpm())

    @Slot(result=bool)
    def is_playing(self):
        return self.__controller.get_pi()

    @Slot(result=bool)
    def error_happened(self):
        return self.__controller.error_happened()

    @Slot(result=str)
    def get_error(self):
        return self.__controller.get_em()

    @Slot(str)
    def read_filename(self, filename):
        self.__controller.change_source(filename)

    @Slot(result=str)
    def get_default_filename(self):
        return self.__controller.get_source()

    @Slot(result=float)
    def get_progress(self):
        return self.__controller.get_progress()

    @Slot(result=str)
    def get_filename(self):
        return self.__controller.get_source_cropped()

    #
    #   Events
    #

    def keyPressEvent(self, q_key_event: QEvent):
        if q_key_event.key() in self.__key_to_id.keys():
            self.__controller.react_on_key_press(self.__key_to_id[q_key_event.key()])
            return True

        super().keyPressEvent(q_key_event)
