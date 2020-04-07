from PySide2.QtCore import QTimer


class Timer:
    @staticmethod
    def __convert_2_local_time(wpm):
        return 60 * 1000 / wpm

    def __init__(self):
        self.__timer = QTimer()

    def start(self, wpm, function):
        self.__timer = QTimer()
        local_time = self.__convert_2_local_time(wpm)
        self.__timer.timeout.connect(function)
        self.__timer.start(local_time)

    def stop(self):
        self.__timer.stop()

    def delete(self):
        self.__timer = None

    def is_active(self):
        return self.__timer and self.__timer.isActive()

    def is_not_deleted(self):
        return self.__timer is not None
