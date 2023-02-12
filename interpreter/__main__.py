# General
import os
import time
from threading import Thread

# External modules
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa

# Interface
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, Gio

# Application
from interpreter import Interpreter
from handler import Handler
import dictionaries as dic


# The Builder class creates the interface objects (widgets) from file
builder = Gtk.Builder()
builder.add_from_file("interface/gui.glade")

# Join signal-response pairs managed by the Handler class
handler = Handler(builder)
builder.connect_signals(handler)

# Load CSS theme
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path("/home/amaldok/Prog/CS-IA/interface/theme.css") # full path needed
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# Load main window
window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit) # Join quit signal to destroy main window
window.show_all()						 # Show all widgets

# Start the main loop
Gtk.main()
