import os
import time

from threading import Thread
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa as mute_alsa

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from interpreter import Interpreter
import dictionaries as dic

cssList = ["RightArrowButton", "LeftArrowButton"]


class Handler():
	"docstring"

	def __init__(self, builder):
		self.interpreter = Interpreter(self.display_spoken_text, self.display_translated_text)
		self.builder = builder
		self.current_idx = -1

		src = self.builder.get_object("SrcLangComboBox")
		dest = self.builder.get_object("DestLangComboBox")
		for i in range(4):
			src.append_text(dic.languages[i])
			dest.append_text(dic.languages[i])
		src.set_active(1)
		dest.set_active(0)

		for name in cssList:
			widget = self.builder.get_object(name)
			widget.set_name(name)

		rArrow = self.builder.get_object("RightArrowButton")
		rArrow.set_sensitive(False)
		lArrow = self.builder.get_object("LeftArrowButton")
		lArrow.set_sensitive(False)
	
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
		srcBuffer.do_insert_text(srcBuffer, i, text, len(text)+1) # O si no se come la ultima letra
		srcTextView = self.builder.get_object("SpokenTextView")
		srcTextView.set_buffer(srcBuffer)

		self.current_idx = self.interpreter.get_size()-1
		rArrow = self.builder.get_object("RightArrowButton")
		rArrow.set_sensitive(False)
		lArrow = self.builder.get_object("LeftArrowButton")
		lArrow.set_sensitive(True)

	def display_translated_text(self, text):
		destBuffer = Gtk.TextBuffer()
		i = destBuffer.get_start_iter()
		destBuffer.do_insert_text(destBuffer, i, text, len(text))
		destTextView = self.builder.get_object("TranslatedTextView")
		destTextView.set_buffer(destBuffer)

	def on_soundbutton_clicked(self, button):
		destTextView = self.builder.get_object("TranslatedTextView")
		destBuffer = destTextView.get_buffer()
		start = destBuffer.get_start_iter()
		end = destBuffer.get_end_iter()
		text = destBuffer.get_text(start, end, False)

		self.interpreter.inter_reproduce(text)

	def on_rightarrow_clicked(self, button):
		sz = self.interpreter.get_size()
		if (self.current_idx + 1 == sz):
			return

		self.current_idx += 1
		lArrow = self.builder.get_object("LeftArrowButton")
		lArrow.set_sensitive(True)
		if (self.current_idx + 1 == sz):
			rArrow = self.builder.get_object("RightArrowButton")
			rArrow.set_sensitive(False)

		srcText = self.interpreter.get_transcribed_text(self.current_idx)
		srcBuffer = Gtk.TextBuffer()
		i = srcBuffer.get_start_iter()
		srcBuffer.do_insert_text(srcBuffer, i, srcText, len(srcText))
		srcTextView = self.builder.get_object("SpokenTextView")
		srcTextView.set_buffer(srcBuffer)

		destText = self.interpreter.get_translated_text(self.current_idx)
		destBuffer = Gtk.TextBuffer()
		i = destBuffer.get_start_iter()
		destBuffer.do_insert_text(destBuffer, i, destText, len(destText))
		destTextView = self.builder.get_object("TranslatedTextView")
		destTextView.set_buffer(destBuffer)

	def on_leftarrow_clicked(self, button):
		sz = self.interpreter.get_size()
		if (self.current_idx - 1 == -1):
			return
			
		self.current_idx -= 1
		rArrow = self.builder.get_object("RightArrowButton")
		rArrow.set_sensitive(True)
		if (self.current_idx == 0):
			lArrow = self.builder.get_object("LeftArrowButton")
			lArrow.set_sensitive(False)

		srcText = self.interpreter.get_transcribed_text(self.current_idx)
		srcBuffer = Gtk.TextBuffer()
		i = srcBuffer.get_start_iter()
		srcBuffer.do_insert_text(srcBuffer, i, srcText, len(srcText))
		srcTextView = self.builder.get_object("SpokenTextView")
		srcTextView.set_buffer(srcBuffer)

		destText = self.interpreter.get_translated_text(self.current_idx)
		destBuffer = Gtk.TextBuffer()
		i = destBuffer.get_start_iter()
		destBuffer.do_insert_text(destBuffer, i, destText, len(destText))
		destTextView = self.builder.get_object("TranslatedTextView")
		destTextView.set_buffer(destBuffer)