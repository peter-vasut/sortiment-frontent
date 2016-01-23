from gi.repository import Gtk


def create_button(text=""):
    return Gtk.Button(text)

def create_user_row(user, callback):
    row = Gtk.ListBoxRow()
    event_box = Gtk.EventBox()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
    label = Gtk.Label(user.get('nick',user.get('name',"???")), xalign=0)
    image = Gtk.Image()
    image.set_from_icon_name("gtk-missing-image", 6)
    hbox.pack_start(image, False, True, 0)
    hbox.pack_start(label, True, True, 0)
    event_box.add(hbox)
    event_box.connect("button_press_event",callback,user)
    row.add(event_box)
    return row