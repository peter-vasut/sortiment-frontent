from gi.repository import Gtk

import sortimentGUI.window_creator
from database import Database

if __name__ == '__main__':
    window = sortimentGUI.window_creator.create_window_main(Database())
    Gtk.main()