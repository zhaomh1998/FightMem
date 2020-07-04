import pickle
import os
import pandas as pd
from datetime import datetime, timedelta


class FightMem:
    def __init__(self, knowledge_file, database_file=None):
        assert os.path.exists(knowledge_file), f'Cannot locate <{knowledge_file}>. Please check!'
        self.knowledge = pickle.load(open(knowledge_file, 'rb'))
        assert isinstance(self.knowledge, pd.DataFrame)

        if database_file is None:
            self.db_path = os.path.splitext(knowledge_file)[0] + '.fmdb'
        else:
            self.db_path = database_file
        if os.path.exists(self.db_path):
            self.db = pickle.load(open(self.db_path, 'rb'))
        else:
            self.db = []



    def get_next_quiz(self):
        """ High level API to get next knowledge """
        print("Getting next quiz item")

    def set_quiz_result(self, id, result):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'later']
        print(f"Setting {id} to {result}")

