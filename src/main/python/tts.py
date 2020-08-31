import os
import time
import traceback
from gtts import gTTS
from PyQt5.QtCore import *
from playsound import playsound


class TTSWorker(QThread):
    def __init__(self, queue, data_fold_path):
        self.storage_folder = os.path.join(data_fold_path, 'tts')
        if not os.path.exists(self.storage_folder):
            assert os.path.exists(data_fold_path), '\'data\' folder not found!'
            os.mkdir(self.storage_folder)

        QThread.__init__(self)
        self.q = queue

    def get_tts(self, text):
        assert isinstance(text, str)
        text_save = text.replace(' ', '_')
        save_file = os.path.join(self.storage_folder, f'{text_save}.mp3')
        if not os.path.exists(save_file):
            tts = gTTS(text, lang='en')
            tts.save(save_file)
        return save_file

    def run(self):
        while True:  # to keep the thread running
            if not self.q.empty():
                msg = self.q.get()
                assert isinstance(msg, str), f'Expected string to be tts\'d! Got {type(msg)}: {msg}'
                try:
                    playsound(self.get_tts(msg))
                except:
                    traceback.print_exc()

            time.sleep(0.1)
