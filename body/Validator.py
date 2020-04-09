class Validator:

    def __init__(self):
        self.__type_to_func = { "wpm" : self.__validate_wpm,
                                "dem" : self.__validate_dem,
                                "ds"  : self.__validate_ds,
                                "zw"  : self.__validate_zw }

    #
    #   Private
    #

    def __validate_wpm(self, value):
        try:
            value = int(value)
        except ValueError as exception:
            raise Validator.ValidationException("Speed value must be int")

        if value < 0:
            raise Validator.ValidationException("Speed cannot be less than 0")

        if value > 10000:
            raise Validator.ValidationException(
                "Speed cannot be more than 10000"
            )

    def __validate_dem(self, value):
        if len(value) == 0:
            raise Validator.ValidationException(
                "Default error message cannot be empty string"
            )

    def __validate_zw(self, value):
        if len(value) == 0:
            raise Validator.ValidationException(
                "Greeting message cannot be empty string"
            )

        if len(value) > 25:
            raise Validator.ValidationException(
                "Too long Greeting. Max len: 25"
            )

    def __validate_ds(self, value):
        pass

    #
    #   Public
    #

    def validate(self, type: str, value):
        if not type in self.__type_to_func.keys():
            raise Validator.InvalidObjectTypeException (
                f"Wrong validation type: '{type}'"
            )

        try:
            self.__type_to_func[type](value)
        except Validator.ValidationException as exception:
            raise Validator.ValidationException(str(exception))

    #
    #   Exceptions
    #

    class InvalidObjectTypeException(Exception):
        pass

    class ValidationException(Exception):
        pass