import sys

from database import Database
from gi.repository import Gtk
from . import window_creator
from .error_handler import catch_global_exception, catch_global_exception_with_gtk_main
from .window_handler import WindowHandler


def main():
    sys.excepthook = catch_global_exception_with_gtk_main
    window_creator.create_window_main(WindowHandler(), Database())
    sys.excepthook = catch_global_exception
    Gtk.main()

if __name__ == '__main__':
    main()
