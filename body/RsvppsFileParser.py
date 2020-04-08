import logging

from body.Validator import Validator


class RsvppsFileParser:

    @staticmethod
    def parse(dictionary, path_to_file: str):
        try:
            with open(path_to_file) as file:
                for line_idx, line in enumerate(file.readlines()):
                    line = line.rstrip()
                    if len(line) == 0:
                        continue

                    try:
                        k, v = RsvppsFileParser.__parse_line(line)
                        dictionary[k] = v
                    except RsvppsFileParser.LineErrorException as exception:
                        logging.warning(f"Error in line {line_idx + 1}. {exception}")
                    except RsvppsFileParser.LineIsCommentException as ignored:
                        pass
        except FileNotFoundError as exception:
            logging.warning("Default setting file not found")
        finally:
            return dictionary

    @staticmethod
    def __parse_line(line: str):
        if len(line) == 0 or line[0] == '#':
            raise RsvppsFileParser.LineIsCommentException
        kv = line.split(':')

        if len(kv) != 2:
            raise RsvppsFileParser.LineErrorException(
                f"Line should contain only one ':'"
                f" symbol, but it contains: {len(kv) - 1}"
            )

        k, v = kv[0].strip().strip("'").strip('"'), kv[1].strip().strip("'").strip('"')

        validator = Validator()
        try:
            validator.validate(k, v)
        except Validator.InvalidObjectTypeException as exception:
            raise RsvppsFileParser.LineErrorException(f"Incorrect key: {k}. {exception}")
        except Validator.ValidationException as exception:
            raise RsvppsFileParser.LineErrorException(f"Incorrect value: {v}. {exception}")

        return k, v

    class LineErrorException(Exception):
        pass

    class LineIsCommentException(Exception):
        pass