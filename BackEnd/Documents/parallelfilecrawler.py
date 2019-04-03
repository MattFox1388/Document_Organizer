import os
import time
from concurrent.futures import Future, ThreadPoolExecutor

from sabackend import SABackend
from document import Document
from documentparser import DocumentParser
from filecrawler import FileCrawler
from storagebackend import StorageBackend
from textractparser import TextractParser
from videoparser import VideoParser

class ParallelFileCrawler(FileCrawler):

    def _parse_file(self, parser: DocumentParser, file_path: str) -> Document:
        return parser.parse(file_path)

    def _submit(self, parser: DocumentParser, file_path: str) -> Future:
        return self._executor.submit(self._parse_file, parser, file_path)

    def crawl(self, path: str):
        futures = self.do_crawl(path)
        for f in futures:
            while not f.done():
                time.sleep(1)
            doc = f.result()
            if doc is not None:
                print(doc.get_file_path())
                print(doc.get_keywords())
                self._get_backend().store([doc])

    def do_crawl(self, path: str):
        futures = []
        for entry in os.listdir(path):
            entry_path = path + "/" + entry
            if os.path.isdir(entry_path):
                futures.extend(self.do_crawl(entry_path))
            else:
                ext = os.path.splitext(entry_path)[1]
                parser = self._get_parser(ext)
                if parser is None:
                    continue
                futures.append(self._submit(parser, entry_path))
        return futures

    def __init__(self, workers: int, backend: StorageBackend):
        super().__init__(backend)
        self._executor = ThreadPoolExecutor(max_workers=workers)


root = '/home/Project/java8doc'

crawler = ParallelFileCrawler(1, SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', \
                                           '5432'))

textp = TextractParser()
crawler.register(textp, '.gif')
#crawler.register_parser(TextractParser())
#crawler.register_parser(VideoParser())

crawler.crawl(root)