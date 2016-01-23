import functools
from time import sleep
import threading
from database import Database
import sortimentGUI.gtk_element_creator


class MainWindowHandler:
    user_image = None
    spinner = None
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
            if self.spinner != None:
                self.spinner.start()
            result = function(self, *args, **kwargs)
            if self.spinner != None:
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
            thread = threading.Thread(target=function,args = tuple([self]+ list(args)),kwargs=kwargs)
            thread.start()
        return inner


    def register_user_image(self, image):
        """
        Function used to register where to put image of selected user.
        :param image: image object
        """
        self.user_image = image

    def register_spinner(self, spinner):
        """
        Function used to register default spinner to indicate running process.
        :param spinner: spinner object
        """
        self.spinner = spinner
        spinner.stop()

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
    def register_food_list(self, list):
        """
        Function used to register graphical list of food.
        :param list: list to register
        """
        self.food_list = list

    def user_selected(self, _, _2, id):
        print("Not implemented", id)

    @use_threading
    @use_spinner
    def update_user_list(self, *args):
        """
        Updates user list with new data from database.
        """
        list = Database.get_user(None)
        print(list)
        for user in list:
            row = sortimentGUI.gtk_element_creator.create_user_row(user, self.user_selected)
            self.user_list.add(row)
        self.user_list.show_all()

    def update_food_list(self, *args):
        pass
    def update_user_image(self, *args):
        pass

    def update(self, *args):
        """
        Updates all data presented in main window.
        """
        self.update_food_list()
        self.update_user_list()
        self.update_user_image()

    def set_database(self,database):
        """
        Sets which database should be used for retrieving data to display.

        :param database: database to use
        """
        self.database = database

