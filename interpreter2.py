import os
import time
from threading import Thread
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import mute_alsa


class Interpreter():
	'docstring. description of the class'

	def __init__(self):
		self.global_status = 'paused'
		self.path = os.getcwd()

		self.src_lang = 'es'
		self.dest_lang = 'en'
		self.transcribed_text = ""
		self.translated_text = ""
		self.code_to_lang = LANGUAGES
		self.lang_to_code = {lang: code for code, lang in LANGUAGES.items()}
		
		self.recognizer = sr.Recognizer()
		self.recognizer.pause_threshold = 1
		self.stop_thread_function = ""
		self.translator = Translator()

	def set_src_lang(self, lang='es'):
		self.src_lang = lang

	def set_dest_lang(self, lang='en'):
		self.dest_lang = lang

	def get_transcribed_text(self):
		return self.transcribed_text
	
	def get_translated_text(self):
		return self.translated_text

	def start(self):
		self.global_status = 'interpreting'
		t = Thread(target=self.interp_recognize)
		t.start()

	def stop(self):
		self.stop_thread_function(wait_for_stop=False)

	def interp_recognize(self):
		if self.global_status == 'paused':
			return

		# m = sr.Microphone(device_index=14, sample_rate=44100)	
		m = sr.AudioFile('rec.wav')
		with m as source:
			self.recognizer.adjust_for_ambient_noise(source)

		self.stop_thread_function = self.recognizer.listen_in_background(m, self.callback)

	def callback(self, recognizer, audio):
			try:
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
				self.transcribed_text = text # Send signal
				self.interp_translate(text)

	def interp_translate(self, text):
		if self.global_status == 'paused':
			return
		translation = self.translator.translate(text, dest=self.dest_lang, src=self.src_lang)
		self.translated_text = translation.text # Send signal	
		self.inter_reproduce(translation.text)

	def inter_reproduce(self, text):
		if self.global_status == 'paused':
			return
		tts = gTTS(text, lang=self.dest_lang)
		tts.save(self.path + '/temp.mp3')
		playsound(self.path + '/temp.mp3')
		os.remove(self.path + '/temp.mp3')
		time.sleep(1)

interpreter = Interpreter()
interpreter.set_src_lang('es')
interpreter.set_dest_lang('en')

interpreter.start()
x = input("Enter something to stop.")
interpreter.stop()

# UnknownValueError at 30 seconds
# WaitTimeoutError also at 30 seconds