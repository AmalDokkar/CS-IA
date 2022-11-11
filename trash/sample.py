# import gi

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk


# class MyWindow(Gtk.Window):
#     def __init__(self):
#         super().__init__(title="Hello World")

#         self.button = Gtk.Button(label="Click Here")
#         self.button.connect("clicked", self.on_button_clicked)
#         self.add(self.button)

#     def on_button_clicked(self, widget):
#         print("PUMMMMM!!! Bye bye world")


# win = MyWindow()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()

import speech_recognition as sr
import interpreter.mute_alsa as mute_alsa

mics = sr.Microphone().list_microphone_names()
print(mics[14])