import os
import time

from threading import Thread
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa

import gi
gi.require_version("Gtk", "3.0") # Really necessary?
from gi.repository import Gtk

from interpreter import Interpreter
from handler import Handlerte

######################################################

interpreter = Interpreter()
handler = Handler()

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()