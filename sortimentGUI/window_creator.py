import os
from database import Database
from gi.repository import Gtk


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
    if handler is not None:
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
                  fullscreen=True, get_objects=None):
    """
    Universal function for creating window.

    :param layout_file_location: path to .glade file containing layout information about window
    :param event_handler: handler used to handle window events
    :param show_all: True if window should be shown immediately
    :param should_quit: True if window should quit after user closed it
    :param relative_filenames: True if layout_file_location should be considered relative to script
    :param fullscreen: True if window should be in full screen mode by default
    :return: returns new window
    """
    builder = Gtk.Builder()
    if relative_filenames:
        layout_file_location = os.path.join(os.path.dirname(__file__), layout_file_location)
    builder.add_from_file(layout_file_location)
    if event_handler is not None:
        builder.connect_signals(event_handler)
    window = builder.get_object("window")

    if get_objects is not None:
        for obj_k in get_objects.keys():
            get_objects[obj_k] = builder.get_object(obj_k)

    if show_all:
        window.show_all()
    if should_quit:
        window.connect("delete-event", Gtk.main_quit)
    if fullscreen:
        window.fullscreen()
    if event_handler is not None:
        event_handler.set_actual_window(window)
    return window


def create_dummy_window(show_all=True, should_quit=False, fullscreen=False):
    """
    Function to create dummy window which does nothing.

    :param show_all: True if window should be shown immediately
    :param should_quit: True if window should quit after user closed it
    :param fullscreen: True if window should be in full screen mode by default
    :return: True if window should be in full screen mode by default
    """

    window = Gtk.Window()
    if show_all:
        window.show_all()
    if should_quit:
        window.connect("delete-event", Gtk.main_quit)
    if fullscreen:
        window.fullscreen()
    return window


def create_window_error(show_all=True, fullscreen=True):
    """
    Creates new error window. Should be used only in case of emeregency.

    :param show_all: True if window should be shown immediately
    :param fullscreen: True if window should be in full screen mode by default
    :return: new window and some objects
    """

    objects = {"cancel_button": None, "textview1": None, "textview2": None, "textview3": None}
    new_window = create_window("layouts/error_window.glade", None, show_all=show_all, should_quit=True,
                               relative_filenames=True, fullscreen=fullscreen, get_objects=objects)
    new_window.set_keep_above(True)
    return new_window, objects


def create_window_edit_profile(handler, show_all=True, fullscreen=True):
    """
    Creates window displaying info about user. It also alows modifying data.

    :param fullscreen: True if window should be in full screen mode by default
    :param handler: Sortiment WindowHandler or None
    :param show_all: True if window should be shown immediately
    :return: new Window
    """

    return create_window("layouts/profile_edit_window.glade", handler, show_all=show_all, should_quit=False,
                         relative_filenames=True, fullscreen=fullscreen)


def create_window_edit_food(handler, show_all=True, fullscreen=True):
    """
    Creates window displaying info about food. It also allows modifying data.

    :param handler: Sortiment WindowHandler or None
    :param show_all: True if window should be shown immediately
    :param fullscreen: True if window should be in full screen mode by default
    :return: ner Window
    """

    return create_window("layouts/item_edit_window.glade", handler, show_all=show_all, should_quit=False,
                         relative_filenames=True, fullscreen=fullscreen)
