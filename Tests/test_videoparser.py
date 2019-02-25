import sys
import unittest
from typing import Collection

sys.path.append("..")

from Documents.videoparser import VideoParser


class TestVideoParser(unittest.TestCase):

    parser = VideoParser()

    def test_can_parse(self):
        self.assertFalse(self.parser.can_parse('video.mp3'))
        self.assertFalse(self.parser.can_parse('mp4'))
        self.assertTrue(self.parser.can_parse('video.mp4'))
        self.assertTrue(self.parser.can_parse('video.MP4'))
        self.assertTrue(self.parser.can_parse('video.MoV'))
        self.assertTrue(self.parser.can_parse('\'video file\'.mp4'))

    def test_getcompatible(self):
        list_compatible_exts = self.parser.get_compatible_extensions()
        self.assertIsInstance(list_compatible_exts, Collection)
        for element in list_compatible_exts:
            self.assertIsInstance(element, str)
        print(list_compatible_exts)

    ''' This test will take a while due to the fact that the parser
        needs to  first extract the audio from the video file.
        Then it needs to transcribe the audio, and finally it iterates
        through transcription to find word occurrences.
    '''
    def test_parser(self):
        pass


if __name__ == '__main__':
    unittest.main()
