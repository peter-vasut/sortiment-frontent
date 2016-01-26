import functools
import threading
from time import sleep

import sortimentGUI.gtk_element_editor
from database import Database


class MainWindowHandler:
    user_image = None
    spinner = None
    task_count = 0
    user_list = None
    food_list = None
    database = None

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
        sortimentGUI.gtk_element_editor.set_listbox_filter(list, self.user_filter)
        self.update_user_list()

    def register_food_list(self, list):
        """
        Function used to register graphical list of food.

        :param list: list to register
        """

        self.food_list = list
        # todo: add food filter
        self.update_food_list()

    def user_selected(self, _, _2, id):
        print("Not implemented", id)  # todo

    def food_selected(self, *args):
        print("Not implmented", args)  # todo

    @use_threading
    @use_spinner
    def update_user_list(self, *args):
        """
        Updates user list with new data from database.

        """

        list = Database.get_user(None)
        for user in list:
            row = sortimentGUI.gtk_element_editor.create_user_row(user, self.user_selected)
            self.user_list.add(row)
        self.user_list.show_all()

    @use_threading
    @use_spinner
    def update_food_list(self, *args):
        """
        Updates food list with new data from database.
        """

        list = Database.get_food(None)
        for food in list:
            row = sortimentGUI.gtk_element_editor.create_food_row(food, self.food_selected)
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
