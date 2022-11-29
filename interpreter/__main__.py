import os
import time

from threading import Thread
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, Gio

from interpreter import Interpreter
from handler import Handler
import dictionaries as dic

######################################################


builder = Gtk.Builder()
builder.add_from_file("interface/gui.glade")

handler = Handler(builder)
builder.connect_signals(handler)

screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path("/home/amaldok/Prog/CS-IA/interface/theme.css")
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()
