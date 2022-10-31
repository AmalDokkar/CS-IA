from threading import Thread
from googletrans import Translator, LANGUAGES
# from speech_recognition import Recognizer, Microphone, AudioFile
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

class Interpreter():
	'docstring. description of the class'

	def __init__(self):
		self.global_status = 'paused'
		self.recognize_satus = 'available'
		self.translate_satus = 'available'
		self.reproduce_satus = 'available'

		self.origin_language = 'es'
		self.destination_language = 'en'
		self.transcribed_text = []
		self.translated_text = []

		self.recognizer = sr.Recognizer()
		self.recognizer.energy_threshold = 100 # Must be adjusted by hand
		self.recognizer.pause_threshold = 1
		self.translator = Translator()
		
	def interpreter_recognize(self):
		with sr.Microphone() as source:
			print("Listening...")
			audio = self.recognizer.listen(source)
			print("Recgonizing...")
			text = self.recognizer.recognize_google(audio, language='es')
			print("Recgonized text:", text)
			self.transcribed_text.append(text)
			self.interpreter_translate(text)

	def interpreter_translate(self, text):
		translation = self.translator.translate(text, dest='de', src='es')
		self.translated_text.append(translation.text)
		print("Translated text:",  translation.text)
		self.interpreter_reproduce(translation.text)

	def interpreter_reproduce(self, text):
		tts = gTTS(text, lang='de')
		tts.save('hola.mp3')
		playsound('hola.mp3')

# print(LANGUAGES)
interpreter = Interpreter()
interpreter.interpreter_recognize()