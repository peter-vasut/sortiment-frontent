from gi.repository import Gtk

from database import Database
from . import window_creator


def main():
    window = window_creator.create_window_main(Database)
    Gtk.main()


if __name__ == '__main__':
    main()
