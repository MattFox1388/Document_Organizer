import sys
import unittest
import time
from typing import Collection

sys.path.append("..")

from Documents.videoparser import VideoParser


class TestVideoParser(unittest.TestCase):

    parser = VideoParser()
    sample_files = []

    def test_can_parse(self):
        self.assertFalse(self.parser.can_parse('video.mp3'))
        self.assertFalse(self.parser.can_parse('mp4'))
        self.assertTrue(self.parser.can_parse('video.mp4'))
        self.assertTrue(self.parser.can_parse('video.MP4'))
        self.assertTrue(self.parser.can_parse('video.MoV'))
        self.assertTrue(self.parser.can_parse('\'video file\'.mp4'))

    def test_get_compatible(self):
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
        for video_file in self.sample_files:
            if self.parser.can_parse(video_file):
                t0 = time.time()
                print('Parsing: ' + video_file + '...')

                doc = self.parser.parse(video_file)
                tf = time.time()
                print(f'It took {(tf-t0)/60} minutes')
                doc.__repr__()


if __name__ == '__main__':
    if len(sys.argv) > 1: # To test individual video files add filenames as arguments (argv). Remember to use spaces
        TestVideoParser.sample_files.append(sys.argv.pop())
    unittest.main()
