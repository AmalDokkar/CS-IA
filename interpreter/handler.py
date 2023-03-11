# General
import os
from threading import Thread

# External modules
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa # REMOVE

# Interface
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, Gio

# Application
from interpreter import Interpreter
import dictionaries as dic

# Widgets that need to be named again for CSS to recognize them
cssList = ["RightArrowButton", "LeftArrowButton"]


class Handler():
	"Handles events (signals) triggered in the GUI by the user"

	def __init__(self, builder):
		# Create instance of Interpreter passing two Handler methods as callbacks
		self.interpreter = Interpreter(self.display_spoken_text, self.display_translated_text)
		self.builder = builder
		self.current_idx = -1 # Index of the translations array (stored in interpreter)

		# Fill comboboxes with language names
		src = self.builder.get_object("SrcLangComboBox")
		dest = self.builder.get_object("DestLangComboBox")
		for i in range(4):
			src.append_text(dic.languages[i])
			dest.append_text(dic.languages[i])
		# Set defaults
		src.set_active(1)
		dest.set_active(0)

		# Rename widgets that have CSS overriden theme (otherwise CSS does not recognize them)
		for name in cssList:
			widget = self.builder.get_object(name)
			widget.set_name(name) # Assign same name

		# Set arrows unsensitive 
		rArrow = self.builder.get_object("RightArrowButton")
		rArrow.set_sensitive(False)
		lArrow = self.builder.get_object("LeftArrowButton")
		lArrow.set_sensitive(False)
	
	# Play/pause button
	def on_toggled_button(self, button):
		active = button.get_active() # Get new status

		# Retrieve widgets to modify
		label = self.builder.get_object("PlayPauseLabel")
		image = self.builder.get_object("PlayPauseImage")
		src = self.builder.get_object("SrcLangComboBox")
		dest = self.builder.get_object("DestLangComboBox")
		switch = self.builder.get_object("SwitchButton")
		sound = self.builder.get_object("SoundButton")
		copy = self.builder.get_object("CopyClipboard")

		if active:
			label.set_text("Pause")
			image.set_from_icon_name("media-playback-pause", 2)
			self.interpreter.start() # Start interpreting

			# Set unsensitive
			src.set_sensitive(False)
			dest.set_sensitive(False)
			switch.set_sensitive(False)
			sound.set_sensitive(False)
			copy.set_sensitive(False)

		else:
			label.set_text("Play")
			image.set_from_icon_name("media-playback-start", 2)
			self.interpreter.stop() # Stop interpreting

			# Set sensitive
			src.set_sensitive(True)
			dest.set_sensitive(True)
			switch.set_sensitive(True)
			sound.set_sensitive(True)
			copy.set_sensitive(True)

	def on_changed_src_lang(self, comboBox):
		lang = comboBox.get_active_text()
		code = dic.lang_to_code[lang]
		self.interpreter.set_src_lang(code) # Change src on Interpreter

	def on_changed_dest_lang(self, comboBox):
		lang = comboBox.get_active_text()
		code = dic.lang_to_code[lang]
		self.interpreter.set_dest_lang(code) # Change dest on Interpreter

	def on_clicked_switch_button(self, button):
		src = self.builder.get_object("SrcLangComboBox")
		dest = self.builder.get_object("DestLangComboBox")

		# Retrieve language and index
		srcIdx = src.get_active()
		srcText = src.get_active_text()
		destIdx = dest.get_active()
		destText = dest.get_active_text()

		# Perform swap
		src.set_active(destIdx)
		dest.set_active(srcIdx)
		self.interpreter.set_src_lang(dic.lang_to_code[destText])
		self.interpreter.set_dest_lang(dic.lang_to_code[srcText])

	def on_clicked_copyclipboard(self, button):
		if self.current_idx != -1:
			text = self.interpreter.get_translated_text(self.current_idx)
			clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
			clipboard.set_text(text, len(text)) # Set text on clipboard

	def display_spoken_text(self, text, newSentence):
		srcBuffer = Gtk.TextBuffer() 							# Create new buffer
		i = srcBuffer.get_start_iter()
		srcBuffer.do_insert_text(srcBuffer, i, text, len(text)) # Put text on buffer
		srcTextView = self.builder.get_object("SpokenTextView")
		srcTextView.set_buffer(srcBuffer) 						# Put buffer on text view

		if newSentence: # Whether it's the last sentence translated by Interpreter (when used as callback)
			self.current_idx = self.interpreter.get_size()-1 	# Set idx to last
			rArrow = self.builder.get_object("RightArrowButton")
			rArrow.set_sensitive(False)
			if (self.current_idx > 0): # If there are previous sentences, allow to navigate back
				lArrow = self.builder.get_object("LeftArrowButton")
				lArrow.set_sensitive(True)

	def display_translated_text(self, text):
		destBuffer = Gtk.TextBuffer() 								# Create new buffer
		i = destBuffer.get_start_iter()
		destBuffer.do_insert_text(destBuffer, i, text, len(text)) 	# Put text on buffer
		destTextView = self.builder.get_object("TranslatedTextView")
		destTextView.set_buffer(destBuffer) 						# Put buffer on text view

	def on_soundbutton_clicked(self, button):
		if self.current_idx != -1:
			# Get text and language at idx (the one at display)
			text = self.interpreter.get_translated_text(self.current_idx)
			lang = self.interpreter.get_trans_text_lang(self.current_idx)
			self.interpreter.interpreter_reproduce(text, lang) # Call Interpreter reproduce method

	def on_rightarrow_clicked(self, button):
		sz = self.interpreter.get_size()
		if (self.current_idx + 1 == sz): # Out of bounds
			return

		self.current_idx += 1
		lArrow = self.builder.get_object("LeftArrowButton")
		lArrow.set_sensitive(True)
		if (self.current_idx + 1 == sz): # If last, set right unsensitive
			rArrow = self.builder.get_object("RightArrowButton")
			rArrow.set_sensitive(False)

		# Get text by index in the lists stored in Interpreter and display
		srcText = self.interpreter.get_transcribed_text(self.current_idx)
		self.display_spoken_text(srcText, False)
		destText = self.interpreter.get_translated_text(self.current_idx)
		self.display_translated_text(destText)

	def on_leftarrow_clicked(self, button):
		sz = self.interpreter.get_size()
		if (self.current_idx - 1 == -1): # Out of bounds
			return
			
		self.current_idx -= 1
		rArrow = self.builder.get_object("RightArrowButton")
		rArrow.set_sensitive(True)
		if (self.current_idx == 0): # If first, set left unsentive
			lArrow = self.builder.get_object("LeftArrowButton")
			lArrow.set_sensitive(False)

		# Get text by index in the lists stored in Interpreter and display
		srcText = self.interpreter.get_transcribed_text(self.current_idx)
		self.display_spoken_text(srcText, False)
		destText = self.interpreter.get_translated_text(self.current_idx)
		self.display_translated_text(destText)