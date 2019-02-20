from typing import Collection

from Documents.documentparser import DocumentParser
from Documents.document import SimpleDocument, Document
import textract
import os.path
import re
from string import punctuation
from collections import Counter

EXTENSIONS = {'.csv', '.doc', '.docx', '.eml', '.epub', '.gif', '.jpg', '.jpeg', '.json', '.html', '.htm', '.mp3',
              '.msg', '.odt', '.ogg', '.pdf', '.png', '.pptx', '.ps', '.rtf', '.tiff', '.tif', '.txt', '.wav', 'xlsx',
              '.xls'}
splitter = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))


class FileParser(DocumentParser):

    def get_compatible_extensions(self) -> Collection[str]:
        pass

    def parse(self, file_path: str) -> Document:
        ext = os.path.splitext(file_path)[1]

        if ext in EXTENSIONS:
            text = textract.process(file_path)
            word_list = splitter.split(text)[:-1]
            word_map = dict(Counter(word_list))
            return SimpleDocument(hash(file_path), word_map, file_path)
        # Need to decide how other files will be parsed
        # if the extension does not exist in EXTENSIONS
        pass
