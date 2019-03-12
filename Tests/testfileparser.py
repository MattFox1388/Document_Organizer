import sys
import unittest
from BackEnd.Documents import TextractParser
from typing import Collection
import os.path

sys.path.append("..")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFileParser(unittest.TestCase):
    parser = TextractParser()

    def test_can_parse(self):
        self.assertFalse(self.parser.can_parse('test1.mp4'))
        self.assertTrue(self.parser.can_parse('test2.csv'))
        self.assertTrue(self.parser.can_parse('test3.png'))
        self.assertTrue(self.parser.can_parse('test4.html'))
        self.assertFalse(self.parser.can_parse('test5.fake'))
        self.assertFalse(self.parser.can_parse('test6.dat'))
        self.assertTrue(self.parser.can_parse('test7.pptx'))
        self.assertTrue(self.parser.can_parse('test8.jpg'))

    def test_get_compatible(self):
        exts = self.parser.get_compatible_extensions()
        self.assertIsInstance(exts, Collection)
        for ele in exts:
            self.assertIsInstance(ele, str)
        print(exts)

    def test_parser(self):
        doc = self.parser.parse(ROOT_DIR+'\\TestFiles\\test.txt')
        self.assertEqual(3, doc.get_occurrences('quick'))
        self.assertEqual(1, doc.get_occurrences('abilities'))

