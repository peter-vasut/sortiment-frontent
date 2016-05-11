def get_user_printable_name(user, errstring="???"):
    user.get('nick', user.get('name', errstring))
