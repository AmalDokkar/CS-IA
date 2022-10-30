from threading import Thread
from googletrans import Translator
import speech_recognition
from gtts import gTTS

class Interpreter():
	"docstring. description of the class"

	def __init__(self):
		self.global_status = "paused"
		self.recognize_satus = "available"
		self.translate_satus = "available"
		self.reproduce_satus = "available"

		self.origin_language = ""
		self.destination_language = ""
		self.transcribed_text = []
		self.translated_text = []

		self.recognizer = speech_recognition.Recognizer()
		self.translator = Translator()
		
	def recognize(self):
		with speech_recognition.Microphone() as source:
			print("Listening...")
			audio = self.recognizer.listen(source)
			print("Transcribing...")
			text = self.recognizer.recognize_google(audio)
			print(text)
			# pass

interpreter = Interpreter()
interpreter.recognize()