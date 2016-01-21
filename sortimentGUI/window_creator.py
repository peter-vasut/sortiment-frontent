from gi.repository import Gtk
from sortimentGUI.main_window_handler import MainWindowHandler

def create_window_main(database=None, show_all=True):
    builder = Gtk.Builder()
    builder.add_from_file("layouts/main_window.glade")
    handler = MainWindowHandler()
    builder.connect_signals(handler)
    window = builder.get_object("window")
    if show_all:
        window.show_all()
    window.connect("delete-event", Gtk.main_quit)
    return window

def create_button(text=""):
    return Gtk.Button(text)