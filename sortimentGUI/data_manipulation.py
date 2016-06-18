import getpass
import string
import unicodedata
from math import sqrt

default_currency = "\u20AC"


def get_universal_printable_name(item, errstring="???"):
    """
    Gets name of user or food in printable form.

    :param item: User or Item object
    :param errstring: string to return if name could not be resolved
    :return: item.nick if exists, item.name otherwise (if exists), errstring if nick and name are missing
    """

    if "nick" in dir(item):
        return get_user_printable_name(item, errstring=errstring)
    else:
        return get_item_printable_name(item, errstring=errstring)


def get_user_printable_name(user, errstring="???"):
    """
    Gets name of user in printable form.

    :param user: user object
    :param errstring: string to return if name could not be resolved
    :return: user.nick if exists, user.name otherwise (if exists), errstring if nick and name are missing
    """

    if user is None:
        return errstring
    return user.nick if (user.nick is not None) else (user.name if (user.name is not None) else errstring)


def get_item_printable_name(item, errstring="???"):
    """
    Gets name of item in printable form.

    :param item: item object
    :param errstring: string to return if name could not be resolved
    :return: item.name if exists, errstring if name is missing
    """

    if item is None:
        return errstring
    res = item.name if (item.name is not None) else errstring
    if item.price is not None:
        res += " (" + str(get_item_price_printable(item)) + ")"
    return res


def get_user_balance_printable(user, currency=default_currency, errstring="???", sep=","):
    """
    Gets balance of user

    :param user: user object
    :param currency: string appended to balance
    :param errstring: string to return if balance could not be resolved
    :param sep: separator for decimal places
    :return: returns user balance, or none on error
    """

    if user is None or user.balance is None:
        return errstring
    return format_money(user.balance, sep, currency)


def get_item_price_printable(item, currency=default_currency, errstring="???", sep=","):
    """
    Gets price of item

    :param item: Item object
    :param currency: string appended to balance
    :param errstring: string to return if balance could not be resolved
    :param sep: separator for decimal places
    :return: returns item price, or none on error
    """
    if item.price is None:
        return errstring
    return format_money(item.price, sep, currency)


def get_all_names(obj):
    """
    Should return all possible names for object, for example real name of user or food, nick...

    :param obj: user or food
    :return: list of strings
    """

    res = list()
    if "name" in dir(obj):
        if obj.name is not None:
            res.append(obj.name)
    if "nick" in dir(obj):
        if obj.nick is not None:
            res.append(obj.nick)

    return res


def normalize_string(s, lowercase=True, special=True):
    output = ''
    if special:
        s = unicodedata.normalize('NFKD', s)
        for c in s:
            if not unicodedata.combining(c):
                if c in string.ascii_letters:
                    output += c
    else:
        output = s
    if lowercase:
        output = output.lower()
    return output


def format_money(number, separator=",", currency=default_currency):
    return ("-" if number < 0 else "") + str(abs(number) // 100) + separator + "{:02d}".format(
        abs(number) % 100) + currency


def expand_username(text):
    return text.replace("%user%", getpass.getuser())


def compute_scaling_factor(awidth, aheight, standard_window_width, standard_window_height):
    return sqrt((min(awidth, aheight) ** 2) / (standard_window_width * standard_window_height))
