import requests
from bs4 import BeautifulSoup
import os
import sys


class Translator:
    user_agent = 'Mozilla/5.0'
    base_url = 'https://context.reverso.net/translation'
    headers = {'User-Agent': user_agent}
    lang_from = None
    lang_into = None
    phrase_to_translate = None
    translated_words = None
    from_context_phrase = None
    into_context_phrase = None
    switch = False
    language_options = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french',
                        '6': 'hebrew', '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese',
                        '11': 'romanian', '12': 'russian', '13': 'turkish'}

    def __init__(self):
        self.set_base_state()

    def set_base_state(self):
        args = sys.argv
        self.lang_from = args[1]
        if args[2] == 'all':
            self.switch = True
        else:
            self.lang_into = args[2]
        self.phrase_to_translate = args[3]

    def main(self):
        if self.switch is not True:
            self.parsing_one()
        else:
            self.parsing_all()
        self.reading()

    def get_url(self, language):
        url = f'{self.base_url}/{self.lang_from}-{language}/{self.phrase_to_translate}'
        return url

    def new_run(self):
        if os.path.exists(f'{self.phrase_to_translate}.txt'):
            os.remove(f'{self.phrase_to_translate}.txt')
        file = open(f'{self.phrase_to_translate}.txt', 'x', encoding='utf-8')
        file.close()

    def file_check(self):
        if os.path.exists(f'{self.phrase_to_translate}.txt'):
            os.remove(f'{self.phrase_to_translate}.txt')
        file = open(f'{self.phrase_to_translate}.txt', 'x', encoding='utf-8')
        file.close()

    def parsing_all(self):
        self.new_run()
        s = requests.Session()
        self.file_check()
        for language in self.language_options.values():
            if language == self.lang_from:
                continue
            try:
                response = s.get(self.get_url(language), headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                self.translated_words = soup.find_all('div', {'id': 'translations-content'})
                self.from_context_phrase = soup.find_all('div', {'class': ['src', 'itr']})
                self.into_context_phrase = soup.find_all('div', {'class': ['trg', 'itr']})
                self.writing(language)
            except requests.exceptions.ConnectionError:
                print("Something wrong with your internet connection")

    def parsing_one(self):
        self.new_run()
        s = requests.Session()
        self.file_check()
        try:
            lang_for_trans = self.language_options[self.lang_into]
            response = s.get(self.get_url(lang_for_trans), headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.translated_words = soup.find_all('div', {'id': 'translations-content'})
            self.from_context_phrase = soup.find_all('div', {'class': ['src', 'itr']})
            self.into_context_phrase = soup.find_all('div', {'class': ['trg', 'itr']})
            self.writing(self.lang_into)
        except requests.exceptions.ConnectionError:
            print("Something wrong with your internet connection")
        except KeyError:
            print(f"Sorry, the program doesn't support {self.lang_into}")

    def writing(self, language):
        translated_word = [t.text.split() for t in self.translated_words]
        from_context_phrase = [e.text.strip('\n ').strip() for e in self.from_context_phrase if e.text.strip()]
        into_context_phrase = [e.text.strip('\n ').strip() for e in self.into_context_phrase if e.text.strip()]
        with open(f'{self.phrase_to_translate}.txt', 'a', encoding='utf-8') as f:
            try:
                f.writelines(f'{language} Translations:\n')
                for word in range(5):
                    f.writelines(translated_word[0][word] + '\n')
                f.writelines('\n')
                f.writelines(f'{language} Examples:\n')
                f.writelines(from_context_phrase[0].strip("'") + '\n')
                f.writelines(into_context_phrase[0].strip("'") + '\n\n\n')
            except IndexError:
                print(f'Sorry, unable to find {self.phrase_to_translate}')

    def reading(self):
        with open(f'{self.phrase_to_translate}.txt', 'r', encoding='utf-8') as f:
            print(f.read())


translator = Translator()
translator.main()
