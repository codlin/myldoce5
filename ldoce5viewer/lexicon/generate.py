from ..cli.ldoce5reader import MyLDOCE5
from .builder import build_phonetic
from .words import WordInfo
from bs4 import BeautifulSoup

WORDS_PATH = "/home/codlin/english_words/coca2w_checked.txt"

ERRWORDS_PATH = "/home/codlin/english_words/coca2w_error.txt"

WORDS_OUTPUT_PATH = "/home/codlin/english_words/coca2w_info_raw.txt"

SAMPLE_AUDIO_PATH = "/home/codlin/english_words/coca2w.media/"

class LexiconFactory:
    def __init__(self):
        self._reader = MyLDOCE5()

        self._load_words(WORDS_PATH)

        self._errwords_handle = open(ERRWORDS_PATH, 'a')
        self._words_output_handle = open(WORDS_OUTPUT_PATH, 'a')

    def __del__(self):
        if self._errwords_handle:
            self._errwords_handle.close()
        if self._words_output_handle:
            self._words_output_handle.close()

    #load word list form laocl file
    #wordspath --absolute path
    def _load_words(self, wordspath):
        file_handle = open(wordspath, 'r')
        self._wordlist = file_handle.readlines()
        file_handle.close()

    def run(self):
        for word in self._wordlist:
            result = self._reader.search(word)
            candidate = self._reader.filter_result(result, word)
            for item in candidate:
                (error, content) = self._reader.load_content(item)
                if error:
                    continue
                #print(content)

                soup = BeautifulSoup(content)
                res = soup.find(class_='hyphenation')
                if res is None:
                    continue

                hyphenation = res.contents[0]
                real_word = word

                #get KK phonetic
                (match, phonetic) = build_phonetic(real_word)
                if match:
                    print(phonetic)
                else:
                    self._errwords_handle.write(real_word)

                Word = WordInfo()
                Word.Name = real_word
                Word.Phonetic = phonetic
                Word.Hyphenation = hyphenation

                res = soup.find(class_='audio', title="American")
                phonetic_audio = res['href'].replace("audio:///", "/")
                _, phonetic_audio_name = phonetic_audio.lstrip('/').split('/', 1)
                (error, audio_content) = self._reader.load_content(phonetic_audio)
                if not error:
                    file_object = open(SAMPLE_AUDIO_PATH + phonetic_audio_name, 'w')
                    file_object.write(audio_content)
                    file_object.close()

                nodes = soup.find_all(class_=["sense", "sense sensewithnum"])
                for node in nodes:
                    if node['class'][0] == "sense":
                        pass

                entry = soup.find(class_='entry')
                for entry_child in entry.children:
                    print(entry_child)
                pass

