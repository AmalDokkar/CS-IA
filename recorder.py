from pyaudio import PyAudio, paInt16
import wave
import time
from threading import Thread

class Recorder():

	def __init__(self):
		self.status = "stop"
		self.frames = []
		self.pa = PyAudio()
		self.rate = 44100
		self.chunck = 2048
		self.format = paInt16
		self.channels = 2


	def start_record(self):
		self.status = "play"
		self.frames = []
		stream = self.pa.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunck)
		while self.status == "play":
		# for i in range(10):
			data = stream.read(self.chunck)
			self.frames.append(data)
			print("* recording")
		
		stream.close()

		wf = wave.open('test_recording.wav', 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(self.pa.get_sample_size(self.format))
		wf.setframerate(self.rate)
		wf.writeframes(b''.join(self.frames))
		wf.close()

	def stop(self):
		self.status = "stop"

rec = Recorder()
t = Thread(target=rec.start_record())
t.start()
time.sleep(2)
t.join()
rec.stop()