import os
import time

from threading import Thread
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, Gio

import dictionaries as dic


class Interpreter():
	"docstring. description of the class"

	def __init__(self, display_spoken_text, display_translated_text):
		self.global_status = "paused"
		self.path = os.getcwd()

		self.src_lang = "es"
		self.dest_lang = "en"
		self.transcribed_texts = [] # ha d'incloure l'idioma
		self.translated_texts = []
		
		self.recognizer = sr.Recognizer()
		self.recognizer.pause_threshold = 1
		self.translator = Translator()

		self.spoken_text_callback = display_spoken_text
		self.translated_text_callback = display_translated_text

	def get_status(self):
		return self.global_status

	def start(self):
		self.global_status = "interpreting"
		t = Thread(target=self.interpreter_recognize)
		t.start()

	def stop(self):
		self.global_status = "paused"

	def set_src_lang(self, lang="es"):
		self.src_lang = lang

	def set_dest_lang(self, lang="en"):
		self.dest_lang = lang

	def get_size(self):
		return len(self.transcribed_texts)

	def get_transcribed_text(self, idx):
		return self.transcribed_texts[idx]

	def get_translated_text(self, idx):
		return self.translated_texts[idx]
		
	def interpreter_recognize(self):
		if self.global_status == "paused":
			return
		# print(sr.Microphone.list_microphone_names())
		# For file
		# with sr.AudioFile("/home/amaldok/Prog/CS-IA/tests/rec.wav") as source:
		# For microphone
		with sr.Microphone(sample_rate=44100, device_index=10) as source:
			try:
				print("Speak now") # Send signal
				# For microphone
				audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
				print("Speech recorded")
				# For file
				# audio = self.recognizer.record(source)
				text = self.recognizer.recognize_google(audio, language=self.src_lang)
				print("Text recognized")
			except sr.WaitTimeoutError:
				print("WaitTimeoutError")
				t = Thread(target=self.interpreter_recognize)
				t.start()
			except sr.UnknownValueError:
				print("UnknownValueError")
				t = Thread(target=self.interpreter_recognize)
				t.start()
			else:
				self.transcribed_texts.append(text)
				self.spoken_text_callback(text, True)
				t = Thread(target=self.interpreter_recognize)
				t.start()
				self.interpreter_translate(text)

	def interpreter_translate(self, text):
		# if self.global_status == 'paused':
		# 	return
		translation = self.translator.translate(text, dest=self.dest_lang, src=self.src_lang)
		print("Text translated")
		text = translation.text
		self.translated_texts.append(text)
		self.translated_text_callback(text)
		self.interpreter_reproduce(text)

	def interpreter_reproduce(self, text):
		# if self.global_status == 'paused':
		# 	return
		tts = gTTS(text, lang=self.dest_lang)
		tts.save(self.path + "/temp.mp3")
		print("Playing audio")
		playsound(self.path + "/temp.mp3")
		print("Audio played")
		os.remove(self.path + "/temp.mp3")