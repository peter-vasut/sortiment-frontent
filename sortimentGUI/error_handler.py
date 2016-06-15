import functools
import sys
import traceback

from gi.repository import Gtk

import window_creator


def show_error(exctype, value, tb, gtk_main=False):
    """
    Shows window showing detailed information about critical error.

    :param exctype: converted to string and displayed (may contain additional text)
    :param value: converted to string and displayed
    :param tb: converted to string and displayed
    :param gtk_main: True if Gtk.main() should be called.
        It can be used if program crashes before main loop is started elsewhere.
    """
    def on_button_clicked(*_):
        window.close()

    window, objects = window_creator.create_window_error()
    cancel_button = objects["cancel_button"]
    cancel_button.connect("clicked", on_button_clicked)
    exctype_textv = objects["textview1"]
    value_textv = objects["textview2"]
    traceback_textv = objects["textview3"]
    exctype_textv.get_buffer().set_text("Exception type: " + str(exctype))
    value_textv.get_buffer().set_text(str(value))
    traceback_textv.get_buffer().set_text("".join(traceback.format_exception(exctype, value, tb)))
    if gtk_main:
        Gtk.main()


def catch_exception(function):
    """
    Can be used to catch any exception and display error message. This shouldn't be used.

    :param function: function to be decorated
    :return: decorated function
    """
    @functools.wraps(function)
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            show_error(*sys.exc_info())

    return inner


def catch_global_exception(exctype, value, tb):
    """
    Shows window showing detailed information about critical error. Also puts standard error message into console.
    It is expected that main Gtk loop is started.
    This can be used as global exception hook.
    See `show_error` function for more details.

    :param exctype: exception type
    :param value: value
    :param tb: traceback
    """
    show_error(exctype, value, tb, gtk_main=False)
    sys.__excepthook__(exctype, value, tb)


def catch_global_exception_with_gtk_main(exctype, value, tb):
    """
    Shows window showing detailed information about critical error. Also puts standard error message into console.
    It is expected that main Gtk loop is not started.
    This can be used as global exception hook.
    See `show_error` function for more details.

    :param exctype: exception type
    :param value: value
    :param tb: traceback
    """
    show_error(exctype, value, tb, gtk_main=True)
    sys.__excepthook__(exctype, value, tb)
