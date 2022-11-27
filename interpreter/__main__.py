import os
import time

from threading import Thread
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa

import gi
gi.require_version("Gtk", "3.0") # Really necessary?
from gi.repository import Gtk, Gio

from interpreter import Interpreter
from handler import Handler
import dictionaries as dic

######################################################

def start_menus(builder):
	src = builder.get_object("SrcLangComboBox")
	dest = builder.get_object("DestLangComboBox")
	for i in range(4):
		src.append_text(dic.languages[i])
		dest.append_text(dic.languages[i])
	src.set_active(1)
	dest.set_active(0)


builder = Gtk.Builder()
builder.add_from_file("interface/gui.glade")

handler = Handler(builder)
builder.connect_signals(handler)

start_menus(builder)

window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()
