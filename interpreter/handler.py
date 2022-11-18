import os
import time

from threading import Thread
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa as mute_alsa

import gi
gi.require_version("Gtk", "3.0") # Really necessary?
from gi.repository import Gtk, Gdk

from interpreter import Interpreter
import dictionaries as dic


def hi():
	print("hello!")

def callback(text):
	print(text)

class Handler():
	"docstring"

	def __init__(self, builder):
		self.interpreter = Interpreter(builder)
		self.builder = builder

	def display_spoken_text(text):
		pass
	
	def on_toggled_button(self, button):
		active = button.get_active()

		if active:
			button.set_label('Pause')
			# self.interpreter.start(hi)
			t = Thread(target=self.interpreter.interp_recognize(), args=(callback,))
			t.start()
		else:
			button.set_label('Play')
			self.interpreter.stop()

	def on_changed_src_lang(self, comboBox):
		lang = comboBox.get_active_text()
		code = dic.lang_to_code[lang]
		self.interpreter.set_src_lang(code)

	def on_changed_dest_lang(self, comboBox):
		lang = comboBox.get_active_text()
		code = dic.lang_to_code[lang]
		self.interpreter.set_dest_lang(code)

	def on_clicked_switch_button(self, button):
		src = self.builder.get_object("SrcLangComboBox")
		dest = self.builder.get_object("DestLangComboBox")

		srcIdx = src.get_active()
		srcText = src.get_active_text()
		destIdx = dest.get_active()
		destText = dest.get_active_text()

		src.set_active(destIdx)
		dest.set_active(srcIdx)
		self.interpreter.set_src_lang(dic.lang_to_code[destText])
		self.interpreter.set_dest_lang(dic.lang_to_code[srcText])