from PySide2.QtCore import Slot, QTimer, Qt, QEvent
from PySide2.QtQuickWidgets import QQuickWidget

from body.Controller import Controller


class Bridge(QQuickWidget):
    def __init__(self, default_source_name=None, default_wpm=250):
        super().__init__()

        # variables for feedback to front
        self.__player_indicator = False
        self.__reading_indicator = False
        self.__error_message = None

        self.__controller = Controller()
        self.__word = self.__default_word = "Space - Start/Stop"
        self.__default_source_name = default_source_name
        self.__timer = None

        self.__change_source(default_source_name)
        self.__controller.set_wpm(default_wpm)


    def __convert_wpm_2_local_time(self, wpm):
        return 60 * 1000 / wpm

    def __start(self):
        if not self.__controller.get_wpm():
            return

        self.__player_indicator = True

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__get_next_word)

        local_time = self.__convert_wpm_2_local_time(self.__controller.get_wpm())

        self.__timer.start(local_time)

    def __stop(self):
        self.__player_indicator = False

        if self.__timer:
            self.__timer.stop()

    def __go_to_start(self):
        self.__word = self.__default_word
        self.__error_message = None
        self.__controller.restart()

        self.__stop()
        self.__timer = None

    def __change_source(self, source):
        player_indicator_copy = self.__player_indicator

        try:
            self.__stop()
            self.__controller.set_source(source)
            self.__go_to_start()
            self.__error_message = None
        except Controller.WrongSourceNameException:
            self.__error_message = "wrong filename"
        finally:
            self.__player_indicator = player_indicator_copy

            if self.__player_indicator:
                self.__start()

    def __get_next_word(self):
        self.__word = self.__controller.get_next_word()

    def __get_previous_word(self):
        self.__word = self.__controller.get_previous_word()

    def __change_speed(self, new_wpm):
        try:
            self.__controller.set_wpm(int(new_wpm))

            if self.__timer and self.__timer.isActive():
                self.__start()
        except Controller.StartTimerException:
            if self.__timer:
                self.__start()
        except Controller.StopTimerException:
            self.__stop()
        except Controller.ValidationException as ignored:
            pass

    def __get_word(self, idx):
        word_len = len(self.__word)

        if word_len == 1:
            orp = 0
        elif word_len < 6:
            orp = 1
        elif word_len < 10:
            orp = 2
        elif word_len < 14:
            orp = 3
        else:
            orp = 4

        before = self.__word[:orp]
        spaces = ' ' * (40 - len(before))
        before = spaces + before

        red_symbol = self.__word[orp]
        after = self.__word[orp + 1:]

        bra = [before, red_symbol, after]

        return bra[idx]

    def get_source(self):
        return self.__controller.get_source()

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
        return self.__get_word(0)

    @Slot(result=str)
    def get_word_B(self):
        return self.__get_word(1)

    @Slot(result=str)
    def get_word_C(self):
        return self.__get_word(2)

    @Slot(result=str)
    def get_wpm(self):
        return str(self.__controller.get_wpm())

    @Slot(result=bool)
    def is_playing(self):
        return self.__player_indicator

    @Slot(result=bool)
    def error_happened(self):
        return self.__error_message is not None

    @Slot(result=str)
    def get_error(self):
        return self.__error_message

    @Slot(result=bool)
    def can_read(self):
        return self.__reading_indicator

    @Slot(str)
    def read_filename(self, filename):
        self.__reading_indicator = False
        self.__change_source(filename)

    @Slot(result=str)
    def get_default_filename(self):
        return self.__default_source_name

    #
    #   Events
    #

    def keyPressEvent(self, q_key_event: QEvent):

        # must react even with error
        if q_key_event.key() == Qt.Key_Alt:
            self.__reading_indicator = True
            return True

        if self.error_happened():
            return super().keyPressEvent(q_key_event)

        # must react only if no errors happened
        if q_key_event.key() == Qt.Key_Space:
            if self.__timer and self.__timer.isActive():
                self.__stop()
            else:
                self.__start()
            return True
        elif q_key_event.key() == Qt.Key_Up:
            self.__change_speed(self.__controller.get_wpm() + 10)
            return True
        elif q_key_event.key() == Qt.Key_Down:
            self.__change_speed(self.__controller.get_wpm() - 10)
            return True
        elif q_key_event.key() == Qt.Key_Left:
            self.__get_previous_word()
            return True
        elif q_key_event.key() == Qt.Key_Right:
            self.__get_next_word()
            return True
        elif q_key_event.key() == Qt.Key_Shift:
            self.__go_to_start()
            return True

        super().keyPressEvent(q_key_event)