import pafy
import vlc
from youtube_dl import YoutubeDL
from requests import get
from AudioFunctions import transcScripter
import json


class YoutubeAudioPlayer:
    def __init__(self):
        self.ins = vlc.Instance()
        self.player = self.ins.media_player_new()

    @staticmethod
    def __search_songs(arg):
        ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
        with YoutubeDL(ydl_options) as ydl:
            try:
                get(arg)
            except:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)
        video = json.dumps(video)
        video = json.loads(video)
        transcScripter.say(video['title'] + ' playing on youtube')
        return video['webpage_url']

    def set_volume(self, volume_number):
        volume_number = int(volume_number) * 10
        if volume_number > 100:
            print("invalid volume")
            transcScripter.say("invalid volume")
            pass
        self.player.volume = volume_number
        json_file_read = open('Config/settings.json', "r")
        print(json_file_read)
        data = json.load(json_file_read)
        data['player']['volume'] = volume_number
        json_file = open('Config/settings.json', "w")
        json_file.write(json.dumps(data, indent=3))
        pass

    @staticmethod
    def __stream(url):
        video = pafy.new(url)
        print('playing... ' + video.title)
        best = video.getbestaudio()
        stream_urls = best.url
        return stream_urls

    def temp_volume(self):
        json_file = open('Config/settings.json', "r")
        data = json.load(json_file)
        if 'playing' in data['player']['current_state']:
            self.player.volume = 1

    def volume_reset(self):
        json_file = open('Config/settings.json', 'r')
        data = json.load(json_file)
        self.player.volume = data['player']['volume']

    def stop(self):
        self.player.stop()
        json_file_read = open('Config/settings.json', "r")
        data = json.load(json_file_read)
        data['player']['current_state'] = 'stopped'
        json_file = open('Config/settings.json', "w")
        json_file.write(json.dumps(data, indent=3))

    def play_functionality(self):
        self.player.play()
        good_states = ["State.Playing", "State.NothingSpecial", "State.Opening"]

        while str(self.player.get_state()) in good_states:
            continue
        self.player.stop()

    def play(self, arg):
        url = self.__search_songs(arg)
        print(url)
        stream_url = self.__stream(url)
        json_file_read = open('Config/settings.json', "r")
        data = json.load(json_file_read)
        data['player']['current_state'] = 'playing'
        print(data)
        json_file = open('Config/settings.json', "w")
        json_file.write(json.dumps(data, indent=3))
        media = self.ins.media_new(stream_url)
        media.get_mrl()
        self.player.set_media(media)
        self.player.volume = data['player']['volume']
        self.play_functionality()
        pass
