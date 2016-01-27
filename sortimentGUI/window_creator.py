from gi.repository import Gtk

from sortimentGUI.main_window_handler import MainWindowHandler


def create_window_main(database=None, show_all=True):
    """
    Creates main window witch user and food list and other elements.

    :param database: database to be used for retrieving user data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    builder = Gtk.Builder()
    builder.add_from_file("layouts/main_window.glade")
    handler = MainWindowHandler()
    builder.connect_signals(handler)
    window = builder.get_object("window")
    if show_all:
        window.show_all()
    window.connect("delete-event", Gtk.main_quit)
    tmp = Gtk.ListBoxRow()
    tmp.event
    return window


def create_window_transaction(database=None, show_all=True, user=dict()):
    """
    Creates transaction window used for transferring money between user and cash, or between two users.

    :param database: database to be used for retrieving data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    pass  # todo


def create_window_profile(database=None, show_all=True):
    """
    Creates window displaying info about user. It also contains button to navigate to transaction window.

    :param database: database to be used for retrieving data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    pass  # todo


def create_window_food(database=None, show_all=True):
    """
    Creates window displaying info about food. It also contains button to navigate to transaction window.

    :param database: database to be used for retrieving data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    pass  # todo
