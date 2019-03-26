import os
import time
from concurrent.futures import Future, ThreadPoolExecutor

from BackEnd.Documents.document import Document
from BackEnd.Documents.documentparser import DocumentParser
from BackEnd.Documents.filecrawler import TFileCrawler, FileCrawler
from BackEnd.Documents.textractparser import TextractParser
from BackEnd.Documents.videoparser import VideoParser


class TParallelFileCrawler(TFileCrawler):
    pass


class ParallelFileCrawler(FileCrawler, metaclass= TParallelFileCrawler):

    def _parse_file(self, parser: DocumentParser, file_path: str) -> Document:
        return parser.parse(file_path)

    def _submit(self, parser: DocumentParser, file_path: str) -> Future:
        return self._executor.submit(self._parse_file, parser, file_path)

    def crawl(self, path: str):
        futures = self.do_crawl(path)
        for f in futures:
            while not f.done():
                time.sleep(2)
            doc = f.result()
            if doc is not None:
                print(f.result().get_keywords)
                #self._get_backend().store(f.result())

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

    def __init__(self, workers: int):
        self._executor = ThreadPoolExecutor(max_workers=workers)


root = 'D:/UWM'

crawler = ParallelFileCrawler(8)
crawler.register_parser(TextractParser())
crawler.register_parser(VideoParser())

crawler.crawl(root)