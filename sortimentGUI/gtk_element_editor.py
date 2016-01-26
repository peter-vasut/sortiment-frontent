from gi.repository import Gtk


def create_button(text=""):
    return Gtk.Button(text)

def create_user_row(user, callback):
    """
    Creates ListBoxRow to display user nick or name and image.

    :param user: user dictionary
    :param callback: function to be called when user is clicked
    :return: new ListBoxRow according to user data and callback function
    """

    row = Gtk.ListBoxRow()
    event_box = Gtk.EventBox()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
    label = Gtk.Label(user.get('nick',user.get('name',"???")), xalign=0)
    image = Gtk.Image()
    image.set_from_icon_name("gtk-missing-image", 6)
    # todo: load real user image
    hbox.pack_start(image, False, True, 0)
    hbox.pack_start(label, True, True, 0)
    event_box.add(hbox)
    event_box.connect("button_press_event",callback,user)
    row.user = user
    row.add(event_box)
    return row


def create_food_row(food, callback):
    """
    Creates ListBoxRow to display food name and image.

    :param food: food dictionary
    :param callback: function to be called when user is clicked
    :return: new ListBoxRow according to user data and callback function
    """

    return create_user_row(food, callback)  # todo: create different row type for food with price tag and edit button


def set_listbox_filter(listbox, filter_function):
    listbox.set_filter_func(filter_function, None)
