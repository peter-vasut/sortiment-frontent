from gi.repository import Gtk

from database import Database
from sortimentGUI.main_window_handler import MainWindowHandler


def create_window_main(database=None, show_all=True):
    """
    Creates main window witch user and food list and other elements.

    :param database: database to be used for retrieving user data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    handler = MainWindowHandler()
    handler.set_database(Database())
    return create_window("layouts/main_window.glade", handler, show_all, True)


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



def create_window_food(database=None, show_all=True):
    """
    Creates window displaying info about food. It also contains button to navigate to transaction window.

    :param database: database to be used for retrieving data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    pass  # todo


def create_window(layout_file_location, event_handler, show_all=True, should_quit=True):
    """
    Universal function for creating window.
    :param layout_file_location: path to .glade file containing layout information about window
    :param event_handler: handler used to handle window events
    :param show_all: True if window should be shown immediately
    :param should_quit: True if window should quit after user closed it
    :return:
    """
    builder = Gtk.Builder()
    builder.add_from_file(layout_file_location)
    builder.connect_signals(event_handler)
    window = builder.get_object("window")
    if show_all:
        window.show_all()
    if should_quit:
        window.connect("delete-event", Gtk.main_quit)
    return window
