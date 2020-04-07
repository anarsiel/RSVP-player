from back.Model import Model
from body.CustomExceptions import CustomClassException


class Controller:

    def __init__(self):
        self.__model = Model()

        self.__wpm = None
        self.__word_idx = -1

        self.__object_types = ["wpm"]

    def __validate(self, value, type: str):
        if not type in self.__object_types:
            raise Controller.InvalidValidationObjectTypeException (
                f"wrong validation type: {type}"
            )

        try:
            if type == "wpm":
                if value < 0:
                    raise Controller.ValidationException()
        except Controller.ValidationException as exception:
            if exception.message:
                raise Controller.ValidationException (
                    f'Inappropriate object value: {type}, {value}'
                )
            else:
                raise exception

    def __get_word(self):
        try:
            return self.__model.get_word(self.__word_idx)
        except Model.EndOfSourceException as exception:
            raise Controller.EndOfSourceException() from exception
        except Model.StartOfSourceException as exception:
            raise Controller.StartOfSourceException from exception

    def get_wpm(self):
        return self.__wpm

    def set_wpm(self, wpm):
        self.__validate(wpm, 'wpm')

        try:
            if wpm == 0:
                raise Controller.StopTimerException()
            elif wpm > 0 and self.__wpm == 0:
                raise Controller.StartTimerException()
        finally:
            self.__wpm = wpm

    def set_source(self, source):
        try:
            self.__word_idx = -1
            self.__model.set_source(source)
            self.__model.upload_data()
        except Model.SourceFileException as exception:
            raise Controller.WrongSourceNameException from exception

    def restart(self):
        self.__word_idx = -1

    def get_next_word(self):
        self.__word_idx += 1
        try:
            return self.__get_word()
        except Controller.EndOfSourceException:
            self.__word_idx -= 1
            return self.__get_word()

    def get_previous_word(self):
        self.__word_idx -= 1
        try:
            return self.__get_word()
        except Controller.StartOfSourceException:
            self.__word_idx += 1
            return self.__get_word()

    def get_source(self):
        self.__model.get_source()

    #
    #   Exceptions
    #

    class WrongSourceNameException(CustomClassException):
        pass

    class StartOfSourceException(CustomClassException):
        pass

    class EndOfSourceException(CustomClassException):
        pass

    class InvalidValidationObjectTypeException(CustomClassException):
        pass

    class ValidationException(CustomClassException):
        pass

    class StopTimerException(CustomClassException):
        pass

    class StartTimerException(CustomClassException):
        pass
