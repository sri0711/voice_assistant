import subprocess
from Config import Self
import json


def is_array_in_string(word_array, input_string):
    for word in word_array:
        if word.lower() in input_string.lower():
            return True
    return False


def replacer(input_string, replacement_words):
    temp = []
    input_string = input_string.split()
    for word in input_string:
        if word not in replacement_words:
            temp.append(word)
    input_string = ' '.join(temp).lower()
    return input_string


def is_online():
    try:
        subprocess.check_output(["ping", "-c", "1", "google.com"])
        return True
    except subprocess.CalledProcessError:
        return False


def get_user_settings():
    json_file = open("Config/settings.json", "r")
    data = json.load(json_file)
    return data
