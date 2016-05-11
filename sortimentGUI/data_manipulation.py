def get_user_printable_name(user, errstring="???"):
    """
    Gets name of user in printable form.
    :param user: user object
    :param errstring: string to return if name could not be resolved
    :return: user['nick'] if exists, user['name'] otherwise (if exists), errstring if 'nick' and 'name' are missing
    """

    return user.get('nick', user.get('name', errstring))


def get_user_balance_printable(user, currency="", errstring="???", sep=","):
    """
    Gets balance of user
    :param user: user object
    :param currency: string appended to balance
    :param errstring: string to return if balance could not be resolved
    :return: returns user balance, or none on error
    """
    if 'balance' not in user:
        return errstring
    return str(user['balance'] // 100) + sep + "{:02d}".format(user['balance'] % 100) + currency
