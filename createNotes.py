from docx import Document
import random
import re
import copy


def set_seed(seed):
    random.seed(seed)


class Notes:
    def __init__(self, raw_notes_path, random_percentage=.5, random_word_percentage=.1, either_symbol_right='~',
                 either_symbol_left='@', blank_symbol='#', seed=None):

        self.random_percentage = random_percentage
        self.random_word_percentage = random_word_percentage
        self.symbol_left = either_symbol_left
        self.symbol_right = either_symbol_right
        self.symbol_rand = blank_symbol
        self.raw_notes = Document(raw_notes_path)

        if seed is not None:
            set_seed(seed)

    def set_randomness(self, random_percentage):
        self.random_percentage = random_percentage

    def set_word_randomness(self, random_percentage):
        self.random_word_percentage = random_percentage

    def either_or(self, text):
        rand = random.random()
        symbol = self.symbol_left if rand > .5 else self.symbol_right  # randomly choose which symbol to blankout

        return self.remove_randomly(text, symbol, 0)

    def remove_randomly(self, text, symbol=None, pattern=None, random_percentage=None):
        if pattern is None:
            pattern = "%s.+?%s" % (symbol, symbol)

        strings_to_remove = []
        for match in re.finditer(pattern, text):
            if random.random() > random_percentage:
                strings_to_remove.append(re.escape(match.group(0)))

        pattern_joined = re.compile("|".join(strings_to_remove))

        return pattern_joined.sub(lambda m: len(m.group(0))*'_', text)

    def remove_random_words(self, text):
        return self.remove_randomly(text, pattern=r'([^\s]+)', random_percentage=1-self.random_word_percentage)

    def remove_symbols(self, text):
        return text.replace(self.symbol_rand, "").replace(self.symbol_right,"").replace(self.symbol_left, "")

    def create_random_notes(self, either_or_flag=True, random_flag=True, random_word_flag=False):
        random_document = copy.copy(self.raw_notes)

        for paragraph in random_document.paragraphs:
            text = paragraph.text
            if either_or_flag:
                text = self.either_or(paragraph.text)
            if random_flag:
                text = self.remove_randomly(text, symbol=self.symbol_rand, random_percentage=self.random_percentage)
            if random_word_flag:
                text = self.remove_random_words(text)
            paragraph.text = self.remove_symbols(text)

        return random_document


if __name__ == '__main__':
    notes = Notes(
        raw_notes_path=r"C:\Users\nickh\Downloads\Interview Notes.docx",
    )
    r_notes = notes.create_random_notes(False, False, True)
    r_notes.save(r"C:\Users\nickh\Downloads\random_notes.docx")
