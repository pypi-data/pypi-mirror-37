"""
Python3 Module

Summary:
    User Input Manipulation

"""
import re
from string import ascii_lowercase


def bool_assignment(arg, patterns=None):
    """
    Summary:
        Enforces correct bool argment assignment
    Arg:
        :arg (*): arg which must be interpreted as either bool True or False
    Returns:
        bool assignment | TYPE:  bool
    """
    arg = str(arg)    # only eval type str
    try:
        if patterns is None:
            patterns = (
                (re.compile(r'^(true|false)$', flags=re.IGNORECASE), lambda x: x.lower() == 'true'),
                (re.compile(r'^(yes|no)$', flags=re.IGNORECASE), lambda x: x.lower() == 'yes'),
                (re.compile(r'^(y|n)$', flags=re.IGNORECASE), lambda x: x.lower() == 'y')
            )
        if not arg:
            return ''    # default selected
        else:
            for pattern, func in patterns:
                if pattern.match(arg):
                    return func(arg)
    except Exception as e:
        raise e


def range_bind(min_value, max_value, value):
    """ binds number to a type and range """
    if value not in range(min_value, max_value + 1):
        value = min(value, max_value)
        value = max(min_value, value)
    return int(value)


def userchoice_mapping(choice):
    """
    Summary:
        Maps the number of an option presented to the user to the
        correct letters in sequential a-z series when choice parameter
        is provided as a number.

        When given a letter as an input parameter (choice is a single
        letter), returns the integer number corresponding to the letter
        in the alphabet (a-z)

        Examples:
            - userchoice_mapping(3) returns 'c'
            - userchoice_mapping('z') returns 26 (integer)
    Args:
        choice, TYPE: int or str
    Returns:
        ascii (lowercase), TYPE: str OR None
    """
    # prepare mapping dict containing all 26 letters
    map_dict = {}
    letters = ascii_lowercase
    for index in range(1, 27):
        map_dict[index] = letters[index - 1]
    # process user input
    try:
        if isinstance(choice, str):
            if choice in letters:
                for k, v in map_dict.items():
                    if v == choice.lower():
                        return k
            elif int(choice) in range(1, 27):
                # integer string provided
                return map_dict[int(choice)]
            else:
                # not in letters or integer string outside range
                return None
        elif choice not in range(1, 27):
            return None
    except KeyError:
        # integer outside range provided
        return None
    except ValueError:
        # string outside range provided
        return None
    return map_dict[choice]
