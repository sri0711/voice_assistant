import nltk
from nltk.metrics.distance import edit_distance
from nltk.corpus import words

nltk.download('all', quiet=True)
correct_words = words.words()


def corrector(incorrect_words):
    print(incorrect_words.split())
    result = ''
    for word in incorrect_words:
        temp = [(edit_distance(word, w), w) for w in correct_words if w[0] == word[0]]
        print(sorted(temp, key=lambda val: val[0])[0][1])
        result = sorted(temp, key=lambda val: val[0])[0][1]
    return result
