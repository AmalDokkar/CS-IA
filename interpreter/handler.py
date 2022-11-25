import os
import time

from threading import Thread
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa as mute_alsa

import gi
gi.require_version("Gtk", "3.0") # Really necessary? yes
from gi.repository import Gtk, Gdk

from interpreter import Interpreter
import dictionaries as dic


class Handler():
	"docstring"

	def __init__(self, builder):
		self.interpreter = Interpreter(self.display_spoken_text, self.display_translated_text)
		self.builder = builder
	
	def on_toggled_button(self, button):
		active = button.get_active()

		if active:
			button.set_label("Pause")
			self.interpreter.start()
		else:
			button.set_label("Play")
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

	def on_clicked_copyclipboard(self, button):
		destTextView = self.builder.get_object("TranslatedTextView")
		destBuffer = destTextView.get_buffer()
		start = destBuffer.get_start_iter()
		end = destBuffer.get_end_iter()
		text = destBuffer.get_text(start, end, False)
		clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		clipboard.set_text(text, len(text))

	def display_spoken_text(self, text):
		srcBuffer = Gtk.TextBuffer()
		i = srcBuffer.get_start_iter()
		srcBuffer.do_insert_text(srcBuffer, i, text, len(text))
		srcTextView = self.builder.get_object("SpokenTextView")
		srcTextView.set_buffer(srcBuffer)

	def display_translated_text(self, text):
		destBuffer = Gtk.TextBuffer()
		i = destBuffer.get_start_iter()
		destBuffer.do_insert_text(destBuffer, i, text, len(text))
		destTextView = self.builder.get_object("TranslatedTextView")
		destTextView.set_buffer(destBuffer)