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

import dictionaries as dic


class Interpreter():
	'docstring. description of the class'

	def __init__(self, builder):
		self.global_status = 'paused'
		self.path = os.getcwd()

		self.src_lang = 'es'
		self.dest_lang = 'en'
		self.transcribed_text = ""
		self.translated_text = ""
		
		self.recognizer = sr.Recognizer()
		self.recognizer.pause_threshold = 1
		self.translator = Translator()

		self.builder = builder

	def get_status(self):
		return self.global_status

	def set_src_lang(self, lang='es'):
		self.src_lang = lang

	def set_dest_lang(self, lang='en'):
		self.dest_lang = lang

	# def get_transcribed_text(self):
	# 	return self.transcribed_text
	
	# def get_translated_text(self):
	# 	return self.translated_text

	def start(self):
		self.global_status = 'interpreting'
		t = Thread(target=self.interp_recognize)
		t.start()

	def stop(self):
		self.global_status = 'paused'
		
	def interp_recognize(self):
		if self.global_status == 'paused':
			return
		
		with sr.AudioFile("/home/amaldok/Prog/CS-IA/tests/rec.wav") as source:
		
		# for linux set device_index = to default
		# with sr.Microphone(sample_rate=44100) as source:
			try:
				print('Speak now') # Send signal
				# For microphone
				# audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
				# For file
				audio = self.recognizer.record(source)
				text = self.recognizer.recognize_google(audio, language=self.src_lang)
			except sr.WaitTimeoutError:
				print('WaitTimeoutError')
				t = Thread(target=self.interp_recognize)
				t.start()
			except sr.UnknownValueError:
				print('UnknownValueError')
				t = Thread(target=self.interp_recognize)
				t.start()
			else:
				self.transcribed_text = text
				self.display_spoken_text()
				t = Thread(target=self.interp_recognize)
				t.start()
				self.interp_translate(text)

	def interp_translate(self, text):
		# if self.global_status == 'paused':
		# 	return
		translation = self.translator.translate(text, dest=self.dest_lang, src=self.src_lang)
		self.translated_text = translation.text
		self.display_translated_text()
		self.inter_reproduce(translation.text)

	def inter_reproduce(self, text):
		# if self.global_status == 'paused':
		# 	return
		tts = gTTS(text, lang=self.dest_lang)
		tts.save(self.path + '/temp.mp3')
		playsound(self.path + '/temp.mp3')
		os.remove(self.path + '/temp.mp3')
		time.sleep(1)

	def display_spoken_text(self):
		srcBuffer = Gtk.TextBuffer()
		i = srcBuffer.get_start_iter()
		srcBuffer.do_insert_text(srcBuffer, i, self.transcribed_text, len(self.transcribed_text))
		srcTextView = self.builder.get_object("SpokenTextBuffer")
		srcTextView.set_buffer(srcBuffer) # ara falla aixo

	def display_translated_text(self):
		destBuffer = Gtk.TextBuffer()
		destBuffer.do_insert_text(0, self.translated_text, len(self.translated_text))
		destTextView = self.builder.get_object("TranslatedTextBuffer")
		destTextView.set_buffer(destBuffer)

# interpreter = Interpreter()
# interpreter.set_src_lang('es')
# interpreter.set_dest_lang('en')

# interpreter.start()
# x = input("Enter something to stop.")
# interpreter.stop()

# UnknownValueError at 30 seconds
# WaitTimeoutError also at 30 seconds