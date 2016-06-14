import os

from gi.repository import Gtk

from database import Database


def create_window_main(handler, database=None, show_all=True):
    """
    Creates main window witch user and food list and other elements.

    :param handler: WindowHandler object
    :param database: database to be used for retrieving user data
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    if database is None:
        database = Database()
    handler.set_database(database)
    return create_window("layouts/main_window.glade", handler, show_all, True)


def create_window_transaction(handler, show_all=True, fullscreen=True):
    """
    Creates transaction window used for transferring money between user and cash, or between two users.

    :param handler: WindowHandler object
    :param show_all: True if window should be shown immediately
    :param fullscreen: True if window should be in full screen mode by default
    :return: new Window
    """

    return create_window("layouts/transaction_window.glade", handler, show_all=show_all, should_quit=True,
                         relative_filenames=True, fullscreen=fullscreen)


def create_window_profile(handler, show_all=True, fullscreen=True):
    """
    Creates window displaying info about user. It also contains button to navigate to transaction window.

    :param fullscreen: True if window should be in full screen mode by default
    :param handler: Sortiment WindowHandler or None
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    return create_window("layouts/profile_window.glade", handler, show_all=show_all, should_quit=False,
                         relative_filenames=True, fullscreen=fullscreen)


def create_window_food(handler, show_all=True, fullscreen=True):
    """
    Creates window displaying info about food. It also contains button to navigate to transaction window.

    :param handler: Sortiment WindowHandler or None
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    pass  # todo


def create_window(layout_file_location, event_handler, show_all=True, should_quit=True, relative_filenames=True,
                  fullscreen=True):
    """
    Universal function for creating window.

    :param layout_file_location: path to .glade file containing layout information about window
    :param event_handler: handler used to handle window events
    :param show_all: True if window should be shown immediately
    :param should_quit: True if window should quit after user closed it
    :param relative_filenames: True if layout_file_location should be considered relative to script
    :param fullscreen: True if window should be in full screen mode by default
    :return:
    """
    builder = Gtk.Builder()
    if relative_filenames:
        layout_file_location = os.path.join(os.path.dirname(__file__), layout_file_location)
    builder.add_from_file(layout_file_location)
    if event_handler is not None:
        builder.connect_signals(event_handler)
    window = builder.get_object("window")
    if show_all:
        window.show_all()
    if should_quit:
        window.connect("delete-event", Gtk.main_quit)
    if fullscreen:
        window.fullscreen()
    if event_handler is not None:
        event_handler.set_actual_window(window)
    return window
