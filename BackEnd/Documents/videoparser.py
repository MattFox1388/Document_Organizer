from documentparser import DocumentParser
from document import Document, SimpleDocument
import os
import utc
import tempfile
from pathlib import Path
import speech_recognition as sr
import moviepy.editor as mp
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

VIDEO_EXTS = {'.flv', '.avi', '.wmv', '.mov', '.mp4', '.wav'}


class VideoParser(DocumentParser):

    def parse(self, file_path: str) -> Document:

        # hash value
        video_hash = self.compute_hash(file_path, 65536)
        file_suffix = Path(file_path).suffix

        # convert video to audio and transcribing audio using speech recognition
        is_audio_already = False
        r = sr.Recognizer()
        if file_suffix != '.wav':
            fd, temp_audio = tempfile.mkstemp('.wav', 'audio')
        else:
            temp_audio = file_path
            is_audio_already = True

        try:
            print(temp_audio)
            # convert video to wav format (sr only supports wav and flac)
            if not is_audio_already:
                VideoParser.convert_video_to_audio(file_path, temp_audio)
            # extract text from temp audio file
            with sr.AudioFile(temp_audio) as source:
                audio = r.record(source)
                text = r.recognize_sphinx(audio)
        finally:
            # get rid of temp audio file if exists
            if not is_audio_already:
                os.remove(temp_audio)

        # filter transcribed text
        word_dict = VideoParser.filter_text(text)

        creat_date, mod_date = SimpleDocument.find_create_and_mod(file_path)

        return SimpleDocument(hash_val=video_hash, keywords=word_dict, file_path=file_path, parse_date=utc.now(),
                              create_date=creat_date, edit_date=mod_date)

    def get_compatible_extensions(self):
        return VIDEO_EXTS

    @staticmethod
    def convert_video_to_audio(video_path, target_audio_path) -> None:

        audio_clip = mp.VideoFileClip(video_path).subclip(0)
        audio_clip.audio.write_audiofile(target_audio_path, nbytes=2)

    @staticmethod
    def filter_text(audio_text):
        # filter transcribed text
        stop_words = set(stopwords.words('english'))
        text_tokens = word_tokenize(audio_text)
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
        return keyword_dict
