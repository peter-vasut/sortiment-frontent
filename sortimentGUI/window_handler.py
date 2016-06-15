from math import sqrt, ceil
from time import sleep

import window_creator
from data_manipulation import get_user_balance_printable
from data_manipulation import get_user_printable_name
from decorators import use_threading, use_spinner
from . import gtk_element_editor


class WindowHandler:
    spinner = None
    task_count = 0
    user_list = None
    food_list = None
    database = None
    selected_food = None
    selected_user = None
    selected_amount = 0
    image_size = 300
    dynamic_scaling_list = list()
    dynamic_font_list = list()
    default_font_factor = 0.05
    window_size = None  # last known window size
    window_history = list()
    actual_window = None  # actual window if known
    user_image_list = list()  # list of all images which should contain profile image of selected user
    user_name_label_list = list()
    user_balance_label_list = list()

    def register_user_image(self, image):
        """
        Function used to register where to put image of selected user.

        :param image: image object
        """
        self.user_image_list.append(image)
        self.update_user_image()

    @use_spinner
    def register_spinner(self, spinner):
        """
        Function used to register default spinner to indicate running process.

        :param spinner: spinner object
        """
        self.spinner = spinner
        if self.task_count > 0:
            spinner.start()

    @use_threading
    @use_spinner
    def spinner_test(self, *_):
        """
        Function used to test spinner as if data were being retrieved from database.
        """

        print("Doing hard work.")
        sleep(5)
        print("Done")

    def register_user_list(self, user_list):
        """
        Function used to register graphical list of users.

        :param user_list: list to register
        """

        self.user_list = user_list
        gtk_element_editor.set_listbox_filter(user_list, self.user_filter)
        self.update_user_list()

    def register_food_list(self, food_list):
        """
        Function used to register graphical list of food.

        :param food_list: list to register
        """

        self.food_list = food_list
        # todo: add food filter
        self.update_food_list()

    def event_user_selected(self, *args):
        self.selected_user = args[2]
        self.update_selected_user_all()

    def event_food_selected(self, *args):
        self.selected_food = args[2]

    @use_threading
    @use_spinner
    def update_user_list(self, *_):
        """
        Updates user user_list with new data from database.
        """

        user_list = self.database.get_user(None)
        for user in user_list:
            row = gtk_element_editor.create_user_row(user, self.event_user_selected, self.register_dynamic_font)
            self.user_list.add(row)
        self.user_list.show_all()

    @use_threading
    @use_spinner
    def update_food_list(self, *_):
        """
        Updates food food_list with new data from database.
        """

        food_list = self.database.get_item(None)
        for food in food_list:
            row = gtk_element_editor.create_food_row(food, self.event_food_selected, self.register_dynamic_font)
            self.food_list.add(row)
        self.food_list.show_all()

    def update_user_image(self, *_):
        for user_image in self.user_image_list:
            gtk_element_editor.image_set_missing(user_image)
            if self.selected_user is not None:
                gtk_element_editor.load_image_from_file(user_image,
                                                        self.selected_user.get('photo', ''),
                                                        self.image_size,
                                                        self.image_size)

    def update_user_name_label(self, *_):
        for user_label in self.user_name_label_list:
            gtk_element_editor.change_label_text(user_label, get_user_printable_name(self.selected_user))

    def update_user_balance_label(self, *_):
        for user_label in self.user_balance_label_list:
            gtk_element_editor.change_label_text(user_label,
                                                 get_user_balance_printable(self.selected_user, currency="€"))

    def update_selected_user_all(self, *_):
        self.update_user_image()
        self.update_user_name_label()
        self.update_user_balance_label()

    def update(self, *_):
        """
        Updates all data presented in main window.
        """

        self.update_food_list()
        self.update_user_list()
        self.update_selected_user_all()

    def set_database(self, database):
        """
        Sets which database should be used for retrieving data to display.

        :param database: database to use
        """

        self.database = database

    def user_filter(self, row, *args):
        """
        Function used to filter users in listbox.

        :param row: row.user should contain valid user dictionary
        :return: True if user should be displayed, False otherwise.
        """
        # todo: implement filter
        return True

    def buy_food(self, *_):
        self.database.buy_items(self.selected_user, self.selected_food, self.selected_amount)
        # todo: error message

    def event_amount_selected(self, *args):
        print(self, args)  # todo

    def window_configure(self, *args):
        """
        Function which should be called on every change of window size.

        :param args First argument should be Gtk.Window or should contain get_size method.
        """

        self.window_size = args[0].get_size()
        self.apply_dynamic_scaling_all(self.window_size[0], self.window_size[1])  # todo: add std. win. width and height
        self.apply_dynamic_font_all(self.default_font_factor, self.window_size[1])

    def register_dynamic_scaling(self, *args):
        """
        Function to be called for registering widget as dynamicly scalable.

        :param args: Argument 0 should be widget do be resized on window change.
        """

        self.dynamic_scaling_list.append((args[0], args[0].props.width_request, args[0].props.height_request))

    @staticmethod
    def apply_dynamic_scaling(awidth, aheight, widget_t, standard_window_width=640, standard_window_height=320):
        """
        Scales specific widget.

        :param awidth: actual window width
        :param aheight: actual window height
        :param widget_t: (widget to scale, original widget width, original widget height)
        :param standard_window_width: standard window width used as reference
        :param standard_window_height: standard window height used as reference
        """

        scaling_factor = sqrt((min(awidth, aheight) ** 2) / (standard_window_width * standard_window_height))
        if widget_t[1] > 0:
            widget_t[0].props.width_request = ceil(widget_t[1] * scaling_factor)
        if widget_t[2] > 0:
            widget_t[0].props.height_request = ceil(widget_t[2] * scaling_factor)

    def apply_dynamic_scaling_all(self, awidth, aheight, standard_window_width=640, standard_window_height=320):
        """
        Scales all widgets registered for dynamic scaling.

        :param awidth: actual window width
        :param aheight: actual window height
        :param standard_window_width: standard window width used as reference
        :param standard_window_height: standard window height used as reference
        """

        for w in self.dynamic_scaling_list:
            self.apply_dynamic_scaling(awidth, aheight, w, standard_window_width, standard_window_height)

    def register_dynamic_font(self, widget, scale=None, *_):
        """
        Function to be called for registering widget containing text to resize and set default font.

        :param widget: widget to be resized on window height change
        :param scale: desired scale (or None)
        """

        if scale is None:
            scale = 1
            try:
                label = widget.props.label
            except AttributeError:
                label = ""
            if "#s:" in label:
                try:
                    scale = int(label[label.find("#s:") + 3:])
                except ValueError:
                    scale = 1

        self.dynamic_font_list.append((widget, scale))
        if self.window_size is not None:
            self.apply_dynamic_font(self.default_font_factor * scale, self.window_size[1], widget)

    @staticmethod
    def apply_dynamic_font(factor, aheight, widget):
        """
        Sets font size on specific widget according to actual window height.

        :param factor: font size divided by window height
        :param aheight: actual window height
        :param widget: widget to setup
        """

        widget.modify_font(gtk_element_editor.create_font_from_description(str(ceil(factor * aheight))))

    def apply_dynamic_font_all(self, factor, aheight):
        """
        Sets font size on registered widgets according to actual window height.

        :param factor: factor * widget scaling factor * aheight = font size
        :param aheight: actual height of window
        """

        for w in self.dynamic_font_list:
            self.apply_dynamic_font(factor * w[1], aheight, w[0])

    def set_actual_window(self, window):
        """
        After creating, event handler should be given reference to window it is handling. It is not required, but when
        it is not set, returning to default window won't work.

        :param window: window which is operating
        """

        self.actual_window = window

    def event_jmp_profile(self, *_):
        """
        Switches current window to profile window.
        """
        if self.selected_user is not None:
            self.window_history.append(self.actual_window)
            self.actual_window.hide()
            self.actual_window = window_creator.create_window_profile(self, self.database)

    def event_jmp_back(self, *_):
        """
        Switches window to previous window on window_history.
        """

        self.actual_window.hide()
        self.actual_window = self.window_history.pop()
        self.actual_window.show()

    def register_user_name(self, label, *_):
        """
        Function to be called for registering GtkLabel for displaying name of selected user.
        """

        self.user_name_label_list.append(label)
        self.update_user_name_label()

    def register_user_balance(self, label, *_):
        """
        Function to be called for registering GtkLabel for displaying name of selected user.
        """

        self.user_balance_label_list.append(label)
        self.update_user_balance_label()

    def event_jmp_transaction(self, *_):
        """
        Switches current window to transaction window.
        """

        print(1 / 0)  # don't try this in production!
        self.window_history.append(self.actual_window)
        self.actual_window.hide()
        self.actual_window = window_creator.create_window_transaction(self, self.database)

    def event_numpad(self, num):
        pass  # todo
