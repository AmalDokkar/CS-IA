# General
import os
from threading import Thread

# External modules
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# Interface
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, Gio

# Application
import dictionaries as dic


class Interpreter():
	"Translates, reproduces sound, stores translation history"

	def __init__(self, display_spoken_text, display_translated_text):
		self.status = "paused"
		self.path = os.getcwd() 			# Full path to temporarily store audio files

		self.src_lang = "es"				# Set defaults
		self.dest_lang = "en"
		self.transcribed_texts = []			# Lists for translations history
		self.translated_texts = []
		self.trans_texts_lang = []
		
		self.recognizer = sr.Recognizer()	# Recognizer instance
		self.recognizer.pause_threshold = 1 # Set time (in seconds) of a pause in speech
		
		# From microphone input devices store index of default
		device_list = sr.Microphone.list_microphone_names()
		self.input_idx = device_list.index("default")	

		self.translator = Translator()		# Translator instace

		# Callbacks to Handler to display text once it is available
		self.spoken_text_callback = display_spoken_text
		self.translated_text_callback = display_translated_text

	# Play/pause
	def start(self):
		self.status = "interpreting"
		t = Thread(target=self.interpreter_recognize)
		t.start()

	def stop(self):
		self.status = "paused"

	# Language setters
	def set_src_lang(self, lang="es"):
		self.src_lang = lang

	def set_dest_lang(self, lang="en"):
		self.dest_lang = lang

	# Translation history getters
	def get_size(self):
		return len(self.transcribed_texts)

	def get_transcribed_text(self, idx):
		return self.transcribed_texts[idx]

	def get_translated_text(self, idx):
		return self.translated_texts[idx]
	
	def get_trans_text_lang(self, idx):
		return self.trans_texts_lang[idx]
		
	# Three important methods:
		# Recognize
		# Translate
		# Reproduce
	
	def interpreter_recognize(self):
		if self.status == "paused":
			return
		
		with sr.Microphone(sample_rate=44100, device_index=self.input_idx) as source:
			try:
				audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5) # Record a phrase
				text = self.recognizer.recognize_google(audio, language=self.src_lang)   # Recognize speech

			except sr.WaitTimeoutError: # User has not spoken within limit time
				print("WaitTimeoutError")
				t = Thread(target=self.interpreter_recognize)
				t.start() # Start new thread

			except sr.UnknownValueError: # Speech is unrecognizable
				print("UnknownValueError")
				t = Thread(target=self.interpreter_recognize)
				t.start() # Start new thread

			else:
				self.transcribed_texts.append(text)		# Update translation history
				self.spoken_text_callback(text, True)	# Display transcribed text
				t = Thread(target=self.interpreter_recognize)
				t.start()								# Start new thread
				self.interpreter_translate(text)		# Continue interpretation process -> translate

	def interpreter_translate(self, text):
		# Translate
		translation = self.translator.translate(text, dest=self.dest_lang, src=self.src_lang)
		text = translation.text

		# Update translation history
		self.translated_texts.append(text)
		self.trans_texts_lang.append(self.dest_lang)
		self.translated_text_callback(text) # Display translated text
		
		self.interpreter_reproduce(text, self.dest_lang) # Reproduce translated text as audio

	def interpreter_reproduce(self, text, lang):
		tts = gTTS(text, lang=lang)			# Get audio
		tts.save(self.path + "/temp.mp3")	# Store temporarily
		playsound(self.path + "/temp.mp3")	# Play 
		os.remove(self.path + "/temp.mp3")	# Erase file