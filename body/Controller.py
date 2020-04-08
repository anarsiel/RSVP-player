from back.Model import Model
from body.RsvppsFileParser import RsvppsFileParser
from body.Validator import Validator
from front.Timer import Timer


class Controller:

    def __init__(self):
        self.__model = Model()
        self.__timer = Timer()
        self.__validator = Validator()

        self.__wpm = None
        self.__source_to_index = {}

        # defaults
        self.__default_dict = {"wpm" : 250,
                               "dem" : " ",
                               "ds"  : "example.txt",
                               "zw"  : "Space - Start/Stop"}

        self.__default_dict = RsvppsFileParser.parse (
            self.__default_dict,
            ".rsvp-player-settings/default.rsvpps"
        )

        self.__default_word = self.__default_dict["zw"]
        self.__source = self.__default_dict["ds"]
        self.set_wpm(int(self.__default_dict["wpm"]))
        self.__default_em = self.__default_dict["dem"]

        self.set_source(self.get_source())
        # variables for front feedback
        self.__word = self.__default_word
        self.__player_indicator = False
        self.__reading_indicator = False
        self.__error_message = self.__default_em

    #
    #   Private
    #

    def __get_word(self):
        try:
            return self.__model.get_word(self.__source_to_index[self.get_source()])
        except Model.EndOfSourceException as exception:
            raise Controller.EndOfSourceException() from exception
        except Model.StartOfSourceException as exception:
            raise Controller.StartOfSourceException from exception

    def __get_orp(self, word_len):
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

        return orp

    #
    #   Public
    #

    def start_playing(self):
        if not self.get_wpm():
            return

        self.set_pi(True)
        self.__timer.start(self.get_wpm(), self.get_next_word)

    def stop_playing(self):
        self.set_pi(False)

        if self.__timer:
            self.__timer.stop()

    def go_to_start(self):
        self.set_word(self.get_default_word())
        self.set_em(None)

        self.__source_to_index[self.get_source()] = -1

        self.stop_playing()
        self.__timer.delete()

    def change_source(self, source):
        if not source or self.__source == source:
            self.set_em(self.__default_dict['dem'])
            return

        pi_copy = self.get_pi()

        try:
            self.stop_playing()

            self.set_source(source)
            self.set_em(None)
            self.set_em(self.__default_dict['dem'])
        except Controller.WrongSourceNameException:
            self.set_em("Wrong filename")

            self.set_pi(pi_copy)
            if self.get_pi():
                self.start_playing()

    def change_speed(self, new_wpm):
        try:
            self.set_wpm(int(new_wpm))

            if self.__timer.is_active():
                self.start_playing()
        except Controller.StartTimerException:
            if self.__timer.is_not_deleted():
                self.start_playing()
        except Controller.StopTimerException:
            self.stop_playing()
        except Validator.ValidationException as ignored:
            pass

    def get_next_word(self):
        self.__source_to_index[self.get_source()] += 1
        try:
            self.set_word(self.__get_word())
        except Controller.EndOfSourceException:
            self.__source_to_index[self.get_source()] -= 1
            self.set_word(self.__get_word())

    def get_previous_word(self):
        self.__source_to_index[self.get_source()] -= 1
        try:
            self.set_word(self.__get_word())
        except Controller.StartOfSourceException:
            self.__source_to_index[self.get_source()] += 1
            self.set_word(self.__get_word())

    def error_happened(self):
        return self.get_em() is not None

    def get_splitted_word(self):
        word_len = len(self.get_word())

        orp = self.__get_orp(word_len)

        before = self.get_word()[:orp]
        spaces = ' ' * (40 - len(before))
        before = spaces + before

        red_symbol = self.get_word()[orp]

        after = self.get_word()[orp + 1:]

        return [before, red_symbol, after]

    def get_progress(self):
        idx = max(self.__source_to_index[self.__source], 0)
        return idx / (self.__model.get_cnt_words() - 1)

    #
    #   Getters - Setters
    #

    def get_word(self):
        return self.__word

    def set_word(self, value):
        self.__word = value

    ####################################

    def get_default_word(self):
        return self.__default_word

    def set_default_word(self, value):
        self.__default_word = value

    ####################################

    def get_ri(self):
        return self.__reading_indicator

    def set_ri(self, value: bool):
        self.__reading_indicator = value

    ####################################

    def get_pi(self):
        return self.__player_indicator

    def set_pi(self, value: bool):
        self.__player_indicator = value

    ####################################

    def get_em(self):
        return self.__error_message

    def set_em(self, value):
        self.__error_message = value

    ####################################

    def get_wpm(self):
        return self.__wpm

    def set_wpm(self, wpm):
        self.__validator.validate('wpm', wpm)

        try:
            if wpm == 0 and self.__wpm is not None:
                raise Controller.StopTimerException()
            elif wpm > 0 and self.__wpm == 0:
                raise Controller.StartTimerException()
        finally:
            self.__wpm = wpm

    ####################################

    def get_source(self):
        return self.__source

    def set_source(self, source):
        try:
            self.__model.set_source(source)

            self.__source = source
            if not source in self.__source_to_index.keys():
                self.__source_to_index[source] = -1
                self.set_word(self.get_default_word())
            else:
                self.set_word(self.__get_word())
        except Model.SourceFileException as exception:
            raise Controller.WrongSourceNameException from exception

    #
    #   Exceptions
    #

    class WrongSourceNameException(Exception):
        pass

    class StartOfSourceException(Exception):
        pass

    class EndOfSourceException(Exception):
        pass

    class InvalidValidationObjectTypeException(Exception):
        pass

    class StopTimerException(Exception):
        pass

    class StartTimerException(Exception):
        pass


