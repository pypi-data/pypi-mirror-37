class Token:

    def __init__(self, word, part_of_speech):
        self.word = word
        self.part_of_speech = part_of_speech

    def __repr__(self):
        return f'{self.word}({self.part_of_speech})'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.word == other.word and self.part_of_speech == other.part_of_speech

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))
