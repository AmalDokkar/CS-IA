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
from gi.repository import Gtk, Gdk

from interpreter import Interpreter


class Handler():

	def __init__(self):
		self.interpreter = Interpreter()
	
	def on_toggled_button(self, button):
		active = button.get_active()

		if active:
			button.set_label('Pause')
			# self.interpreter.start()
		else:
			button.set_label('Play')
			# self.interpreter.stop()