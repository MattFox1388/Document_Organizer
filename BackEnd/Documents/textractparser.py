import textract
import os.path
import utc
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from document import Document, SimpleDocument
from documentparser import DocumentParser

EXTENSIONS = {'.csv', '.doc', '.docx', '.eml', '.epub', '.gif', '.jpg', '.jpeg', '.json', '.html', '.htm', '.mp3',
              '.msg', '.odt', '.ogg', '.pdf', '.png', '.pptx', '.ps', '.rtf', '.tiff', '.tif', '.txt', '.wav', 'xlsx',
              '.xls'}


class TextractParser(DocumentParser):

    def get_compatible_extensions(self):
        return EXTENSIONS

    """
    Removes text from in front of the extension and then checks
    to see if the extension is compatible. If not compatible, it
    is sent to where it can be parsed. Otherwise, the file
    is processed into text using textract. The text is then split
    into a list such that each word is separated and no punctuation
    exists.
    Stop words are removed from the list and then it is put into a dictionary
    """
    def parse(self, file_path: str) -> Document:
        ext = os.path.splitext(file_path)[1]

        if ext not in EXTENSIONS:
            # Need to decide how other files will be parsed
            # if the extension does not exist in EXTENSIONS
            #
            # Also need to find out what other files exist
            # Need to parse through the collection of data
            # and pull each extension to determine this
            return None
        else:
            file_size = os.path.getsize('C:\\Python27\\Lib\\genericpath.py')

            text = textract.process(file_path)
            text = text.decode('utf-8')
            word_list = word_tokenize(text)
            word_list = [''.join(c for c in s if c not in punctuation) for s in word_list]
            word_list = [s for s in word_list if s]
            word_list = [e.lower() for e in word_list]

            total_words = len(word_list)

            stop = set(stopwords.words('english'))
            tokens = [w for w in word_list if not w in stop]
            word_map = dict(Counter(tokens))
            file_hash = int(self.compute_hash(file_path, 65536), 16)
            create, edit = SimpleDocument.find_create_and_mod(file_path)
            return SimpleDocument(hash_val=file_hash, keywords=word_map, file_path=file_path, parse_date=utc.now(),
                                  create_date=create, edit_date=edit, file_size=file_size, total_words=total_words)
