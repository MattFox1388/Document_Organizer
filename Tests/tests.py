import unittest

from Documents.document import Document
from Documents.documentbackend import DocumentBackend
from Documents.documentparser import DocumentParser


class TestBaseAPI(unittest.TestCase):

    def _getParser(self) -> DocumentParser:
        return self._parser

    def _getBackend(self) -> DocumentBackend:
        return self._backend

    def setUp(self):
        self._parser = None
        self._backend = None

    def tearDown(self):
        self._getBackend().close()

    def test_parser(self):
        expected_keywords = {}
        path = ''
        expected_hash = 123
        expected_doc = Document(expected_hash, expected_keywords, path)

        parser = self._getParser()
        self.assertIsNotNone(parser, 'Parser is None!')

        doc = parser.parse(path)
        self.assertIsNotNone(doc, 'Parser returned None instead of a Document instance!')

        self.assertEquals(path, doc.get_file_path())
        self.assertEquals(expected_keywords, doc.get_keywords())
        self.assertEquals(expected_hash, doc.get_hash())

    def test_backend(self):
        key = 'CoolKeyword'
        keywords = (key,25)
        back = self._getBackend()
        self.assertIsNotNone(back, 'Backend is None!')
        doc = Document(0, keywords, '')
        back.store([doc])

        docs = back.get(keywords)
        self.assertTrue(len(docs) > 0, 'No documents with the keyword found!')
        back_doc = None
        for d in docs:
            if doc.is_same(d):
                back_doc = d
                break
        self.assertIsNotNone(back_doc, 'Could not find document in backend!')
        self.assertEquals(doc, back_doc, 'Same document does not equal original!')

        self.assertTrue(back.remove(back_doc))

        docs = back.get(keywords)
        self.assertFalse(back_doc in docs, 'Document is still in backend!')
