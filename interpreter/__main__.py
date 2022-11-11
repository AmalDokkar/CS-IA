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
from gi.repository import Gtk, Gio

from interpreter import Interpreter
from handler import Handler
from dictionaries import * # try import dictionaries as dic

######################################################

def start_languge_menus(menu):
	menuModel = Gio.Menu()
	for i in range(5):
		menuModel.append(languages[i])
	menu.set_menu_model(menuModel)

# interpreter = Interpreter()
handler = Handler()

builder = Gtk.Builder()
builder.add_from_file("interface/gui.glade")
builder.connect_signals(Handler())

src_Menu = builder.get_object("SourceLanguageMenu")
start_languge_menus(src_Menu)

window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()
