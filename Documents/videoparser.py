from typing import Collection

from Documents.documentparser import DocumentParser
from .document import Document, SimpleDocument
import os
import utc
import speech_recognition as sr
import moviepy.editor as mp
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

VIDEO_EXTS = {'.flv', '.avi', '.wmv', '.mov', '.mp4'}


class VideoParser(DocumentParser):

    def parse(self, file_path: str) -> Document:
        # hash value
        video_hash = self.compute_hash(file_path, 65536)

        # converting video to audio
        temp_audio_file = 'audio.wav'
        audio_clip = mp.VideoFileClip(file_path).subclip(0)
        audio_clip.audio.write_audiofile(temp_audio_file, nbytes=2)

        # transcribing audio using speech recognition
        r = sr.Recognizer()
        with sr.AudioFile(temp_audio_file) as source:
            audio = r.record(source)
            text = r.recognize_sphinx(audio)

        # get rid of temporary audio file
        os.remove('audio.wav')
        # filter stopwords
        stop_words = set(stopwords.words('english'))
        text_tokens = word_tokenize(text)
        text_wo_tokens = [word for word in text_tokens if not word in stop_words]

        # only keep words greater than 2
        keyword_dict = dict()
        for item in text_wo_tokens:
            if len(item) > 2:
                # searching dict for keyword and updating
                if item in keyword_dict:
                    keyword_dict[item] += 1
                else:
                    keyword_dict[item] = 1

        creat_date, mod_date = SimpleDocument.find_create_and_mod(file_path)

        return SimpleDocument(hash_val=video_hash, keywords=keyword_dict, file_path=file_path, parse_date=utc.now(),
                              create_date=creat_date, edit_date=mod_date)

    def get_compatible_extensions(self) -> Collection[str]:
        return VIDEO_EXTS
