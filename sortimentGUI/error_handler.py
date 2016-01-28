import functools
import sys

from gi.repository import Gtk


def show_error(parent_window, text):  # todo: not working in parallel?
    dialog = Gtk.MessageDialog(parent=parent_window,
                               flags=Gtk.DialogFlags.MODAL,
                               type=Gtk.MessageType.ERROR,
                               buttons=Gtk.ButtonsType.CANCEL,
                               message_format=text)
    dialog.show_all()


def catch_exception(function):
    @functools.wraps(function)
    def inner(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except:
            show_error(Gtk.Window(), sys.exc_info())

    return inner
