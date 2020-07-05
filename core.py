import pickle
import os
import pandas as pd
from datetime import datetime, timedelta
import ebisu


class FightMem:
    def __init__(self, knowledge_file, database_file=None):
        assert os.path.exists(knowledge_file), f'Cannot locate <{knowledge_file}>. Please check!'
        self.knowledge_path = knowledge_file
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
        entry['score'] = round(ebisu.predictRecall(
            prior=entry['model'],
            tnow=_time_diff_to_hr(entry['t_last'], datetime.now()),
            exact=True
        ), 4)
        return entry

    def new_entry(self, entry_id, total=0, correct=0, start_model=(4., 4., 12)):
        data = self.knowledge.loc[entry_id].to_dict()
        self.db['eb_data'] = self.db['eb_data'].append({
            'id': entry_id,
            'word': data['word'],
            'model': start_model,
            'total': total,
            'correct': correct,
            't_last': datetime.now(),
            'score': 1
        }, ignore_index=True)

    def get_next_quiz(self):
        """ High level API to get next knowledge """
        print("Getting next quiz item")
        self.refresh_db_prediction()
        if self.db['eb_data'].shape[0] != 0 and self.db['eb_data'].iloc[0]['score'] < 0.8:
            self.current_id = self.db['eb_data'].iloc[0, 'id']
            entry = self.knowledge.iloc[self.current_id]
        else:
            new_word_id = self.db['new_words'].pop()
            entry = self.knowledge.iloc[new_word_id]
            self.current_id = new_word_id

        return entry['word'], entry['pron'], entry['mean'], entry['syn'], entry['ex'], entry['note']

    def set_quiz_result(self, result, note_updated):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'later', 'trash', 'init']
        if result != 'init':
            print(f"Setting {self.current_id} to {result}, new note {note_updated}")
            self.knowledge.loc[self.current_id, 'note'] = note_updated

            if any(self.db['eb_data']['id'] == self.current_id):  # Word in EB Database
                item = self.db['eb_data'][self.db['eb_data']['id'] == self.current_id]
                item['t_last'] = datetime.now()
                if result == 'yes':
                    item['total'] += 1
                    item['correct'] += 1
                elif result == 'no':
                    item['total'] += 1
                elif result == 'later':
                    pass
                elif result == 'trash':
                    self.db['eb_data'].drop(item.index, inplace=True)
                self.refresh_db_prediction()
            else:  # Add to EB Database
                if result == 'yes':
                    self.new_entry(self.current_id, total=1, correct=1)
                elif result == 'no':
                    self.new_entry(self.current_id, total=1, correct=0)
                elif result == 'later':
                    self.new_entry(self.current_id, total=1, correct=1)
                elif result == 'trash':
                    pass  # Does not add to review list

            self.save()

    def save(self):
        pickle.dump(self.knowledge, open(self.knowledge_path, 'wb'))
        pickle.dump(self.db, open(self.db_path, 'wb'))


def _time_diff_to_hr(time_a, time_b):
    one_hour = timedelta(hours=1)
    return abs((time_a - time_b) / one_hour)
