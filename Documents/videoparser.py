from Documents.documentparser import DocumentParser
from Documents.document import Document
import subprocess as subpros

class VideoParser(DocumentParser):
    def can_parse(self, file_path: str) -> bool:
        pass

    def parse(self, file_path: str) -> Document:
        pass
