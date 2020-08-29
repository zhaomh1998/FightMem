import os
import time
from gtts import gTTS
from PyQt5.QtCore import *
from playsound import playsound

storage_folder = os.path.join(os.path.curdir, 'data', 'tts')
if not os.path.exists(storage_folder):
    assert os.path.exists(os.path.join(os.path.curdir, 'data')), '\'data\' folder not found!'
    os.mkdir(storage_folder)


def get_tts(text):
    assert isinstance(text, str)
    text_save = text.replace(' ', '_')
    save_file = os.path.join(storage_folder, f'{text_save}.mp3')
    if not os.path.exists(save_file):
        tts = gTTS(text)
        tts.save(save_file)
    return save_file


class TTSWorker(QThread):
    def __init__(self, queue):
        QThread.__init__(self)
        self.q = queue

    def run(self):
        while True:  # to keep the thread running
            if not self.q.empty():
                msg = self.q.get()
                assert isinstance(msg, str), f'Expected string to be tts\'d! Got {type(msg)}: {msg}'
                playsound(get_tts(msg))

            time.sleep(0.1)


if __name__ == '__main__':
    playsound(get_tts('hello'))
