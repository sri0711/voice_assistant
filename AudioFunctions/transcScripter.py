import speech_recognition as sr
import pyttsx4
from gtts import gTTS
import os
from CommonFunctions import utils
from Features.youtubeAudioPlayer import YoutubeAudioPlayer


def take_command(timeout_thresh_hold=10, audio_player=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        # if utils.get_user_settings()['player']['current_state'] == 'playing':
        #     audio_player = YoutubeAudioPlayer()

        try:
            print("Listening...")
            audio = r.listen(source, timeout=timeout_thresh_hold, phrase_time_limit=5)
            if audio_player:
                audio_player.temp_volume()
            query = r.recognize_google(audio, language='en-IN')
            if audio_player:
                audio_player.volume_reset()
            print(query.lower())
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand")
            return "none"
        except sr.RequestError as e:
            print("Could not request results from Google Speech")
            return "none"
        except sr.WaitTimeoutError:
            print("Could not request results from Google Speech because its timeout")
            return "timeout"


def get_available_voices():
    engine = pyttsx4.init()
    voices = engine.getProperty('voices')
    ind_voice = []
    for voice in voices:
        if "IN" in voice.languages[0]:
            ind_voice.append(voice)
    return ind_voice


def say_pyttsx(text):
    engine = pyttsx4.init('')
    voice = get_available_voices()
    engine.setProperty('rate', 160)
    engine.setProperty('pitch', 0.9)
    engine.setProperty('voice', voice[0].id)
    engine.say(text)
    engine.runAndWait()


def say_google(text):
    tts = gTTS(text=text, lang='ta')
    file = "temp.mp3"
    tts.save(file)
    os.system('afplay ' + file)
    os.remove(file)


def say(text):
    if utils.is_online():
        say_google(text)
    else:
        say_pyttsx(text)
