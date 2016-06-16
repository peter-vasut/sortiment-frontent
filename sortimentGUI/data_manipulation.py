import string
import unicodedata


def get_user_printable_name(user, errstring="???"):
    """
    Gets name of user in printable form.

    :param user: user object
    :param errstring: string to return if name could not be resolved
    :return: user['nick'] if exists, user['name'] otherwise (if exists), errstring if 'nick' and 'name' are missing
    """

    return user.nick if (user.nick is not None) else (user.name if (user.name is not None) else errstring)


def get_user_balance_printable(user, currency="", errstring="???", sep=","):
    """
    Gets balance of user

    :param user: user object
    :param currency: string appended to balance
    :param errstring: string to return if balance could not be resolved
    :param sep: separator for decimal places
    :return: returns user balance, or none on error
    """
    if user.balance is None:
        return errstring
    return str(user.balance // 100) + sep + "{:02d}".format(user.balance % 100) + currency


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
