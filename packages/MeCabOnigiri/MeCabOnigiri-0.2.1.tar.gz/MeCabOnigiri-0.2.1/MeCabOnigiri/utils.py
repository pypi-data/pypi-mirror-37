from .tagger import get_mecab_tagger
from .models import Token


def get_word_list(text):
    tagger = get_mecab_tagger('-Ochasen')

    words = []
    node = tagger.parseToNode(text)

    # 最初は捨てる (BOS/EOS)
    node = node.next
    while node:
        splitted = node.feature.split(',')
        word = node.surface
        part_of_speech = splitted[0]
        if part_of_speech == 'BOS/EOS':
            break
        token = Token(word=word, part_of_speech=part_of_speech)
        words.append(token)
        node = node.next

    return words
