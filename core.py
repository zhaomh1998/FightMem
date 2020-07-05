import pickle
import os
import pandas as pd
from datetime import datetime, timedelta
import ebisu


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
            self.db = {
                'eb_data': pd.DataFrame(columns=['id', 'word', 'model', 'total', 'correct', 't_last', 'score']),
                'new_words': set(range(self.knowledge.shape[0]))
            }

        self.current_id = None

    def get_eb(self):
        return self.db['eb_data'][['word', 'score', 'model']]

    def refresh_db_prediction(self):
        self.db['eb_data'] = self.db['eb_data'].apply(self.update_prediction_one_entry, axis=1)
        self.db['eb_data'].sort_values(by='score', ascending=True, inplace=True)

    def update_prediction_one_entry(self, entry):
        entry['score'] = ebisu.predictRecall(
            prior=entry['model'],
            tnow=_time_diff_to_hr(entry['t_last'], datetime.now()) + 5,
            exact=True
        )
        return entry

    def new_entry(self, entry_id, start_model=(4., 4., 12)):
        data = self.knowledge.iloc[entry_id].to_dict()
        self.db['eb_data'] = self.db['eb_data'].append({
            'id': entry_id,
            'word': data['word'],
            'model': start_model,
            'total': 0,
            'correct': 0,
            't_last': datetime.now(),
            'score': 1
        }, ignore_index=True)

    def get_next_quiz(self):
        """ High level API to get next knowledge """
        assert self.current_id is not None
        print("Getting next quiz item")
        self.refresh_db_prediction()
        if self.db['eb_data'].shape[0] != 0 and self.db['eb_data'].iloc[0, 'score'] < 0.8:
            entry = self.knowledge.iloc[self.db['eb_data'].iloc[0, 'id']]
        else:
            new_word_id = self.db['new_words'].pop()
            entry = self.knowledge.iloc[new_word_id]

        return entry['word'], entry['pron'], entry['mean'], entry['syn'], entry['ex'], entry['note']

    def set_quiz_result(self, result, note_updated):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'later', 'trash', 'init']
        if result == 'init':
            self.current_id = 0
        print(f"Setting {self.current_id} to {result}, new note {note_updated}")


def _time_diff_to_hr(time_a, time_b):
    one_hour = timedelta(hours=1)
    return abs((time_a - time_b) / one_hour)
