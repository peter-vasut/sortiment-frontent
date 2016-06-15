import functools
import threading


def use_spinner(function):
    """
    Decorator activating spinner before function and deactivating it.
    (Needs to be ran in separate thread.)

    :param function: function to decorate
    :return: decorated function
    """

    @functools.wraps(function)
    def inner(self, *args, **kwargs):
        self.task_count += 1
        if self.spinner is not None:
            self.spinner.start()
        result = function(self, *args, **kwargs)
        self.task_count = max(self.task_count - 1, 0)
        if self.spinner is not None:
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
