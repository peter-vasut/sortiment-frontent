import functools
import threading
from math import sqrt, ceil
from time import sleep

from . import gtk_element_editor


class MainWindowHandler:
    user_image = None
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

    def use_spinner(function):
        """
        Decorator activating spinner before function and deactivating it.
        (Needs to be ran in separate thread.)

        :param function: function to decorate
        :return: decorated function
        """

        @functools.wraps(function)
        def inner(self, *args, **kwargs):
            if self.spinner == None:
                print("Object", self, "has no spinner registred.")
            self.task_count += 1
            if self.spinner != None:
                self.spinner.start()
            result = function(self, *args, **kwargs)
            self.task_count = max(self.task_count - 1, 0)
            if self.spinner != None:
                if self.task_count == 0:
                    self.spinner.stop()
            return result
        return inner

    def use_threading(function):
        """
        Decorator which runs function in separate thread.
        :return:
        """

        @functools.wraps(function)
        def inner(self, *args, **kwargs):
            thread = threading.Thread(target=function, args=tuple([self] + list(args)), kwargs=kwargs)
            thread.start()

        return inner

    def register_user_image(self, image):
        """
        Function used to register where to put image of selected user.

        :param image: image object
        """
        self.user_image = image

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
    def spinner_test(self, *args):
        """
        Function used to test spinner as if data were being retrieved from database.
        """

        print("Doing hard work.")
        sleep(5)
        print("Done")

    def register_user_list(self, list):
        """
        Function used to register graphical list of users.

        :param list: list to register
        """

        self.user_list = list
        gtk_element_editor.set_listbox_filter(list, self.user_filter)
        self.update_user_list()

    def register_food_list(self, list):
        """
        Function used to register graphical list of food.

        :param list: list to register
        """

        self.food_list = list
        # todo: add food filter
        self.update_food_list()

    def user_selected(self, *args):
        self.selected_user = args[2]
        gtk_element_editor.image_set_missing(self.user_image)
        gtk_element_editor.load_image_from_file(self.user_image,
                                                self.selected_user.get('photo', ''),
                                                self.image_size,
                                                self.image_size)

    def food_selected(self, *args):
        self.selected_food = args[2]

    @use_threading
    @use_spinner
    def update_user_list(self, *args):
        """
        Updates user list with new data from database.

        """

        list = self.database.get_user(None)
        for user in list:
            row = gtk_element_editor.create_user_row(user, self.user_selected)
            self.user_list.add(row)
        self.user_list.show_all()

    @use_threading
    @use_spinner
    def update_food_list(self, *args):
        """
        Updates food list with new data from database.
        """

        list = self.database.get_item(None)
        for food in list:
            row = gtk_element_editor.create_food_row(food, self.food_selected)
            self.food_list.add(row)
        self.food_list.show_all()

    def update_user_image(self, *args):
        # todo
        pass

    def update(self, *args):
        """
        Updates all data presented in main window.
        """

        self.update_food_list()
        self.update_user_list()
        self.update_user_image()

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

    def buy_food(self, *args):
        self.database.buy_items(self.selected_user, self.selected_food, self.selected_amount)
        # todo: error message

    def amount_selected(self, *args):
        print(args)  # todo

    def window_configure(self, *args):
        """
        Function which should be callen on every change of window size.
        """

        window_size = args[0].get_size()
        self.apply_dynamic_scaling(window_size[0], window_size[1])  # todo: add std. win. width and height
        self.apply_dynamic_font(self.default_font_factor, window_size[1])

    def register_dynamic_scaling(self, *args):
        """
        Function to be called for registering widget as dynamicly scalable.

        :param args: Argument 0 should be widget do be resized on window change.
        """

        self.dynamic_scaling_list.append((args[0], args[0].props.width_request, args[0].props.height_request))

    def apply_dynamic_scaling(self, awidth, aheight, standard_window_width=640, standard_window_height=320):
        """
        Scales all widgets registered for dynamic scaling.

        :param awidth: actual window width
        :param aheight: actual window height
        :param standard_window_width: standard window width used as reference
        :param standard_window_height: standard window height used as reference
        """
        scaling_factor = sqrt((min(awidth, aheight) ** 2) / (standard_window_width * standard_window_height))
        for w in self.dynamic_scaling_list:
            if w[1] > 0:
                w[0].props.width_request = ceil(w[1] * scaling_factor)
            if w[2] > 0:
                w[0].props.height_request = ceil(w[2] * scaling_factor)

    def register_dynamic_font(self, widget, *args):
        """
        Function to be called for registering widget containing text to resize and set default font.

        :param widget: widget to be resized on window height change
        """

        self.dynamic_font_list.append(widget)

    def apply_dynamic_font(self, factor, aheight):
        """
        Sets default font on registered widgets according to actual window height.

        :param factor: fotnt size divided by actual window height
        :param aheight: actual height of window
        """

        for w in self.dynamic_font_list:
            w.modify_font(gtk_element_editor.create_font_from_description(str(ceil(factor * aheight))))
