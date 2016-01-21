import functools
from time import sleep
import threading
from database import Database
import sortimentGUI.window_creator

class MainWindowHandler:
    user_image = None
    spinner = None
    user_list = None
    food_list = None
    database = None

    def use_spinner(function):
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
        @functools.wraps(function)
        def inner(self, *args, **kwargs):
            thread = threading.Thread(target=function,args = tuple([self]+ list(args)),kwargs=kwargs)
            thread.start()
        return inner


    def register_user_image(self, image):
        self.user_image = image

    def register_spinner(self, spinner):
        self.spinner = spinner
        spinner.stop()

    @use_threading
    @use_spinner
    def spinner_test(self, widget):
        print("Doing hard work.")
        sleep(5)
        print("Done")

    def register_user_list(self, list):
        self.user_list = list
    def register_food_list(self, list):
        self.food_list = list

    @use_threading
    @use_spinner
    def update_user_list(self, *args):
        list = Database.get_user(None)
        print(list)
        for user in list:
            print("not implemented")

    def update_food_list(self, *args):
        pass
    def update_user_image(self, *args):
        pass

    @use_threading
    @use_spinner
    def update(self, *args):
        self.update_food_list()
        self.update_user_list()
        self.update_user_image()

    def set_database(self,database):
        self.database = database