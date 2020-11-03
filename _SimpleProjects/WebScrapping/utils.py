import re, string

class UtilsFunction():
    def __init__(self):
        pass

    def clean_text_round(self, text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def clean_text_round_second(self, text):
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text

    def textCombination(self, list_of_text):
        combined_text = ''.join(list_of_text)
        return combined_text
