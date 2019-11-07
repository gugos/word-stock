import requests
import re
from bs4 import BeautifulSoup


class Model:
    def get_word_definition(self, word):
        return self.meaning(word)

    '''
    Next method was copied and modified from PyDictionary module https://github.com/geekpradd/PyDictionary
    '''
    @staticmethod
    def meaning(term):
        if len(term.split()) > 1:
            return False, 'Error: A Term must be only a single word'
        else:
            try:
                html = BeautifulSoup(requests.get(f'http://wordnetweb.princeton.edu/perl/webwn?s={term}').text,
                                     'html.parser')
                types = html.findAll('h3')
                lists = html.findAll('ul')
                out = {}
                for word_type in types:
                    reg = str(lists[types.index(word_type)])
                    meanings_list = []
                    for meaning in re.findall(r'\((.*?)\)', reg):
                        if 'often followed by' in meaning:
                            pass
                        elif len(meaning) > 5 or ' ' in str(meaning):
                            meanings_list.append(meaning)
                    name = word_type.text
                    out[name] = meanings_list
                return True, out
            except Exception as ex:
                return False, f'Error: The Following Error occurred: {ex}'
