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

def start_languge_menus(srcMenu, destMenu):
	menuModel = Gio.Menu()
	for i in range(4):
		menuModel.append(languages[i])
	srcMenu.set_menu_model(menuModel)
	destMenu.set_menu_model(menuModel)

# interpreter = Interpreter()
handler = Handler()

builder = Gtk.Builder()
builder.add_from_file("interface/gui.glade")
builder.connect_signals(Handler())

srcMenu = builder.get_object("SourceLanguageMenu")
destMenu = builder.get_object("DestinationLanguageMenu")
start_languge_menus(srcMenu, destMenu)

window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()
