import requests
import re
from bs4 import BeautifulSoup


class Model:
    def __init__(self):
        self.tag_pattern = re.compile(r'<.*?>')

    def get_word_definition(self, word):
        return self.meaning(word)

    '''
    Next method was copied and modified from PyDictionary module https://github.com/geekpradd/PyDictionary
    '''
    def meaning(self, term):
        if len(term.split()) > 1:
            return False, 'Error: A Term must be only a single word'
        else:
            try:
                html = BeautifulSoup(requests.get(f'http://wordnetweb.princeton.edu/perl/webwn?s={term}').text,
                                     'html.parser')
                types = html.findAll('h3')
                lists = html.findAll('ul')
                if not lists:
                    text = re.sub(self.tag_pattern, '', str(types[0]))
                    return False, f'error: {text}'
                out = {}
                for word_type in types:
                    text = re.sub(self.tag_pattern, '', str(lists[types.index(word_type)]))
                    meanings = text.split('\n')
                    meanings_list = []
                    for meaning in meanings:
                        if not meaning or 'often followed by' in meaning:
                            continue
                        meaning = meaning.replace('(', '', 1)
                        first_index = meaning.find('(')
                        last_index = meaning.rfind(')')
                        meanings_list.append(meaning[first_index + 1:last_index])
                    name = word_type.text
                    out[name] = meanings_list
                return True, out
            except Exception as ex:
                return False, f'Error: The Following Error occurred: {ex}'
