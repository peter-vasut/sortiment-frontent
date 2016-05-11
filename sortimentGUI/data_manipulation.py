def get_user_printable_name(user, errstring="???"):
    """
    Gets name of user in printable form.
    :param user: user object
    :param errstring: string to return if name could not be resolved
    :return: user['nick'] if exists, user['name'] otherwise (if exists), errstring if 'nick' and 'name' are missing
    """

    return user.get('nick', user.get('name', errstring))
