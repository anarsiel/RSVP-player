class Validator:

    def __init__(self):
        self.__type_to_func = {"wpm": self.__validate_wpm}

    #
    #   Private
    #

    def __validate_wpm(self, value):
        if value < 0:
            raise Validator.ValidationException("Speed cannot be less than 0")

    #
    #   Public
    #

    def validate(self, type: str, value):
        if not type in self.__type_to_func.keys():
            raise Validator.InvalidObjectTypeException (
                f"wrong validation type: {type}"
            )

        try:
            self.__type_to_func[type](value)
        except Validator.ValidationException as exception:
            if hasattr(exception, 'message'):
                raise Validator.ValidationException(
                    f'Inappropriate object value. {type}: {value}'
                )
            else:
                raise exception

    #
    #   Exceptions
    #

    class InvalidObjectTypeException(Exception):
        pass

    class ValidationException(Exception):
        pass