import model


class Controller:
    def __init__(self):
        self.model = model.Model()

    def get_word_definition(self, word):
        return self.model.get_word_definition(word)
