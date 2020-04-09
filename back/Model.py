import re


class Model:

    def __init__(self, source=None):
        self.__source = source
        self.__words = None

    def set_source(self, source):
        try:
            self.__source = source
            self.upload_data()
        except Model.SourceFileException as exception:
            raise exception

    def upload_data(self):
        if not self.__source:
            raise Model.SourceFileException("Source file is None")

        try:
            with open(self.__source) as file:
                self.__words = list(filter(None, re.split("[ \n]+", file.read())))
        except FileNotFoundError as exception:
            raise Model.SourceFileException(f"Source file {self.__source} doesn't exists") from exception

    def get_word(self, idx):
        if self.__words:
            try:
                if idx == -2:
                    raise Model.GreetingException()

                if idx == -1:
                    raise Model.StartOfSourceException()

                return self.__words[idx]
            except IndexError as exception:
                raise Model.EndOfSourceException() from exception

        raise Model.EndOfSourceException("Data not uploaded."
                                   "You must firstly upload_data()")

    def get_source(self):
        return self.__source

    def get_cnt_words(self):
        if self.__words:
            return len(self.__words)
        return 239

    #
    #   Exceptions
    #

    class SourceFileException(Exception):
        pass

    class EndOfSourceException(Exception):
        pass

    class StartOfSourceException(Exception):
        pass

    class GreetingException(Exception):
        pass

