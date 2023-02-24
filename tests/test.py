import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1

print(sr.Microphone.list_microphone_names())

with sr.Microphone(sample_rate=44100, device_index=10) as source:
    try:
        print("Speak now")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
        print("Speech recorded")
        text = recognizer.recognize_google(audio, language="es")
    except sr.WaitTimeoutError:
        print("WaitTimeoutError")
    except sr.UnknownValueError:
        print("UnknownValueError")
    else:
        print(text)

# Theoretically, a confusing sentence for STT
# "Let's wreck a nice beach" and "Let's recognize speech"

# UnknownValueError at 30 seconds
# WaitTimeoutError also at 30 seconds

# JUST IN CASE I MESS UP
# 	def interpreter_recognize(self):
# 		if self.global_status == "paused":
# 			return
# 		# print(sr.Microphone.list_microphone_names())
# 		# For file
# 		# with sr.AudioFile("/home/amaldok/Prog/CS-IA/tests/rec.wav") as source:
# 		# For microphone
# 		with sr.Microphone(sample_rate=44100, device_index=10) as source:
# 			try:
# 				print("Speak now") # Send signal
# 				# For microphone
# 				audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
# 				print("Speech recorded")
# 				# For file
# 				# audio = self.recognizer.record(source)
# 				text = self.recognizer.recognize_google(audio, language=self.src_lang)
# 				print("Text recognized")
# 			except sr.WaitTimeoutError:
# 				print("WaitTimeoutError")
# 				t = Thread(target=self.interpreter_recognize)
# 				t.start()
# 			except sr.UnknownValueError:
# 				print("UnknownValueError")
# 				t = Thread(target=self.interpreter_recognize)
# 				t.start()
# 			else:
# 				self.transcribed_texts.append(text)
# 				self.spoken_text_callback(text, True)
# 				t = Thread(target=self.interpreter_recognize)
# 				t.start()
# 				self.interpreter_translate(text)

# 	def interpreter_translate(self, text):
# 		# if self.global_status == 'paused':
# 		# 	return
# 		translation = self.translator.translate(text, dest=self.dest_lang, src=self.src_lang)
# 		print("Text translated")
# 		text = translation.text
# 		self.translated_texts.append(text)
# 		self.trans_texts_lang.append(self.dest_lang)
# 		self.translated_text_callback(text)
# 		self.interpreter_reproduce(text, self.dest_lang)

# 	def interpreter_reproduce(self, text, lang):
# 		# if self.global_status == 'paused':
# 		# 	return
# 		tts = gTTS(text, lang=lang)
# 		tts.save(self.path + "/temp.mp3")
# 		print("Playing audio")
# 		playsound(self.path + "/temp.mp3")
# 		print("Audio played")
# 		os.remove(self.path + "/temp.mp3")