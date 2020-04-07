from PySide2.QtCore import Slot, QTimer, Qt, QEvent
from PySide2.QtQuickWidgets import QQuickWidget

from body.Controller import Controller


class Bridge(QQuickWidget):
    def __init__(self):
        super().__init__()

        self.__controller = Controller()

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

    @Slot(result=bool)
    def can_read(self):
        return self.__controller.get_ri()

    @Slot(str)
    def read_filename(self, filename):
        self.__controller.set_ri(False)
        self.__controller.set_source(filename)

    @Slot(result=str)
    def get_default_filename(self):
        return self.__controller.get_source()

    #
    #   Events
    #

    def keyPressEvent(self, q_key_event: QEvent):

        # must react even with error
        if q_key_event.key() == Qt.Key_Alt:
            self.__controller.set_ri(True)
            return True

        if self.error_happened():
            return super().keyPressEvent(q_key_event)

        # must react only if no errors happened
        if q_key_event.key() == Qt.Key_Space:
            # if self.__timer and self.__timer.isActive():
            if self.__controller.get_pi():
                self.__controller.stop_playing()
            else:
                self.__controller.start_playing()
            return True
        elif q_key_event.key() == Qt.Key_Up:
            self.__controller.change_speed(self.__controller.get_wpm() + 10)
            return True
        elif q_key_event.key() == Qt.Key_Down:
            self.__controller.change_speed(self.__controller.get_wpm() - 10)
            return True
        elif q_key_event.key() == Qt.Key_Left:
            self.__controller.get_previous_word()
            return True
        elif q_key_event.key() == Qt.Key_Right:
            self.__controller.get_next_word()
            return True
        elif q_key_event.key() == Qt.Key_Shift:
            self.__controller.go_to_start()
            return True

        super().keyPressEvent(q_key_event)