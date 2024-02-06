from AudioFunctions import transcScripter
from CommonFunctions import utils
from Config import Self
from threading import Thread
from Features.youtubeAudioPlayer import YoutubeAudioPlayer

if __name__ == '__main__':
    while True:
        audio_player = YoutubeAudioPlayer()
        print("setting up audio for environment")
        initialSetupForVoice = transcScripter.take_command()
        if "none" in initialSetupForVoice:
            print("system all are ready you can command now")
            transcScripter.say("Hi Thambi kutty!")
            time_out_input = 30
            while True:
                print("waiting for your command!...")
                voice_input = transcScripter.take_command(time_out_input)
                # voice_input2 = nlp_correcter.correct_words(voice_input)
                # print(voice_input2)

                if utils.is_array_in_string(Self.my_names(), voice_input):
                    if "stop" in voice_input:
                        audio_player.stop()
                        continue
                    if utils.is_array_in_string(Self.volume_const(), voice_input):
                        print("volume set to {}".format(voice_input))
                        voice_input = utils.replacer(voice_input, Self.my_names())
                        voice_input = utils.replacer(voice_input, Self.volume_const())
                        audio_player.set_volume(voice_input)
                    transcScripter.say("How can i help you sri.")

                    command_input = transcScripter.take_command(time_out_input)
                    if "what" in command_input:
                        transcScripter.say("its not yet developed")
                        continue
                    if "play" in command_input:
                        transcScripter.say("wait")
                        play_thread = Thread(target=audio_player.play, args=(command_input,))
                        play_thread.start()
                        continue
