import gi

gi.require_version("Gtk", "3.0") # Really necessary?
from gi.repository import Gtk


class Handler():
	
	def on_toggled_button(self, button):
		active = button.get_active()

		if active:
			button.set_label('Pause')
			# interpreter do stuff
		else:
			button.set_label('Play')
			# interpreter stop doing stuff