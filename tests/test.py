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