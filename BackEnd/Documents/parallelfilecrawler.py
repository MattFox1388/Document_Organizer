import os
import traceback
import time
from concurrent.futures import Future, ThreadPoolExecutor

from sabackend import SABackend
from document import Document
from documentparser import DocumentParser
from filecrawler import FileCrawler
from storagebackend import StorageBackend
from textractparser import TextractParser


class ParallelFileCrawler(FileCrawler):

    @staticmethod
    def is_temp_file(path: str) -> bool:
        return '/~$' in path

    def log(self, message: str, print_std: bool = True):
        if print_std:
            print(message)
        if not message.endswith('\n'):
            message = message + '\n'
        self._file_stream.write(message)

    def finish_log(self):
        self._file_stream.close()

    def _parse_file(self, parser: DocumentParser, file_path: str) -> Document:
        try:
            if self._get_backend().get_by_path(file_path) is None:
                return parser.parse(file_path)
            return None
        except:
            traceback.print_exc()
            print('Error parsing: ' + file_path)
            self.log(file_path, False)
            return None

    def _submit(self, parser: DocumentParser, file_path: str) -> Future:
        return self._executor.submit(self._parse_file, parser, file_path)

    def crawl(self, path: str):
        futures = self.do_crawl(path)
        while futures:
            f = futures.pop(0)
            while not f.done():
                time.sleep(1)
            doc = f.result()
            if doc is not None:
                print('Parsed ' + doc.get_file_path())
                self._get_backend().store([doc])
        self.finish_log()

    def do_crawl(self, path: str):
        futures = []
        for entry in os.listdir(path):
            if entry.startswith('~$'):
                continue
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

    def stop(self):
        self._executor.shutdown(wait=False)

    def __init__(self, workers: int, backend: StorageBackend, log_file: str):
        super().__init__(backend)
        self._executor = ThreadPoolExecutor(max_workers=workers)
        self._file_stream = open(log_file, 'w+')


def sig_handler(sig, frame):
    crawler.stop()

if __name__ == "__main__":
    root = '/home/Project/Data'

    _back = SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', '5432', pool_size=100)
    crawler = ParallelFileCrawler(8, _back, '/home/Project/failed')

    crawler.register_parser(TextractParser())
    #crawler.register_parser(VideoParser())

    #signal.signal(signal.SIGINT, sig_handler)

    crawler.crawl(root)