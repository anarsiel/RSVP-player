from PySide2.QtCore import QTimer


class Timer:
    @staticmethod
    def __convert_2_local_time(wpm):
        return 60 * 1000 / wpm

    def __init__(self):
        self.__timer = QTimer()

    def start(self, time, function, make_conversion=True):
        self.__timer = QTimer()

        if make_conversion:
            time = self.__convert_2_local_time(time)

        self.__timer.timeout.connect(function)
        self.__timer.start(time)

    def stop(self):
        self.__timer.stop()

    def delete(self):
        self.__timer = None

    def is_active(self):
        return self.__timer and self.__timer.isActive()

    def is_not_deleted(self):
        return self.__timer is not None
