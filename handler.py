import gi

gi.require_version("Gtk", "3.0") # Really necessary?
from gi.repository import Gtk


class Handler():

	def onDestroy(self):
		Gtk.main_quit()


builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

window = builder.get_object("MainWindow")
window.show_all()

Gtk.main()