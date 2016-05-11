from gi.repository import Gtk

from database import Database
from . import window_creator
from .window_handler import WindowHandler


def main():
    window_creator.create_window_main(WindowHandler(), Database())
    Gtk.main()


if __name__ == '__main__':
    main()
