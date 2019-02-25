from typing import Collection

from Documents.documentparser import DocumentParser
from Documents.document import SimpleDocument, Document
import textract
import os.path
import re
import utc
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

EXTENSIONS = {'.csv', '.doc', '.docx', '.eml', '.epub', '.gif', '.jpg', '.jpeg', '.json', '.html', '.htm', '.mp3',
              '.msg', '.odt', '.ogg', '.pdf', '.png', '.pptx', '.ps', '.rtf', '.tiff', '.tif', '.txt', '.wav', 'xlsx',
              '.xls'}
splitter = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))


class FileParser(DocumentParser):

    def get_compatible_extensions(self) -> Collection[str]:
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
            pass
        else:
            text = textract.process(file_path)
            word_list = splitter.split(text)[:-1]
            stop = set(stopwords.words('english'))
            tokens = [w for w in word_list if not w in stop]
            word_map = dict(Counter(tokens))
            file_hash = int(self.compute_hash(file_path, 65536), 16)
            return SimpleDocument(hash_val=file_hash, keywords=word_map, file_path=file_path, parse_date=utc.now())
