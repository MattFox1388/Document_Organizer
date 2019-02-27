import os
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Collection

from Documents.document import Document
from Documents.documentparser import DocumentParser
from Documents.filecrawler import TFileCrawler, FileCrawler
from Documents.textractparser import TextractParser
from Documents.videoparser import VideoParser


class TParallelFileCrawler(TFileCrawler):
    pass


class ParallelFileCrawler(FileCrawler, metaclass= TParallelFileCrawler):

    def _parse_file(self, parser: DocumentParser, file_path: str) -> Document:
        print("file path = " + file_path)
        return parser.parse(file_path)

    def _submit(self, parser: DocumentParser, file_path: str) -> Future:
        return self._executor.submit(self._parse_file, parser, file_path)

    def crawl(self, path: str):
        futures = self.do_crawl(path)
        print(len(futures))
        for f in futures:
            while not f.done():
                time.sleep(2)
            print(f.result().get_hash())

    def do_crawl(self, path: str) -> Collection[Future]:
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


root = ''

crawler = ParallelFileCrawler(8)
crawler.register_parser(TextractParser())
crawler.register_parser(VideoParser())

crawler.crawl(root)