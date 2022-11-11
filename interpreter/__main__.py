import os
import time

from threading import Thread
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import interpreter.mute_alsa as mute_alsa

import gi
gi.require_version("Gtk", "3.0") # Really necessary?
from gi.repository import Gtk

from interpreter.interpreter import Interpreter
from interpreter.handler import Handler
from dictionaries import * # try import dictionaries as dic

######################################################


# interpreter = Interpreter()
handler = Handler()

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

# src_comboBox = builder.get_object("SourceLanguageComboText")
# dest_comboBox = builder.get_object("DestinationLanguageComboText")
# for lang in languages:
# 	src_comboBox.append_text(lang)
# 	dest_comboBox.append_text(lang)

window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()