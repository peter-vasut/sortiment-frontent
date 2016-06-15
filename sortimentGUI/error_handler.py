import functools
import sys
import traceback

from gi.repository import Gtk

import window_creator


def show_error(exctype, value, tb, gtk_main=False):
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
    @functools.wraps(function)
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            show_error(*sys.exc_info())

    return inner


def catch_global_exception(exctype, value, tb):
    show_error(exctype, value, tb, gtk_main=False)
    sys.__excepthook__(exctype, value, tb)


def catch_global_exception_with_gtk_main(exctype, value, tb):
    show_error(exctype, value, tb, gtk_main=True)
    sys.__excepthook__(exctype, value, tb)
