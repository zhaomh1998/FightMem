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
        self.db['eb_data'] = self.db['eb_data'].apply(self.eb_update_score, axis=1)
        self.db['eb_data'].sort_values(by='score', ascending=True, inplace=True)
        self.db['eb_data'].reset_index(drop=True, inplace=True)

    def eb_update_score(self, entry):
        entry['score'] = round(ebisu.predictRecall(
            prior=entry['model'],
            tnow=_time_diff_to_hr(entry['t_last'], datetime.now()),
            exact=True
        ), 4)
        return entry

    def new_entry(self, entry_id, total=0, correct=0, start_model=(3., 3., 0.5)):
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
        self.refresh_db_prediction()
        stat = dict()
        if self.db['eb_data'].shape[0] != 0 and self.db['eb_data'].iloc[0]['score'] < 0.8:
            self.current_id = self.db['eb_data'].iloc[0]['id']
            entry = self.knowledge.loc[self.current_id]
            stat['is_new'] = False
            stat['rate'] = self.db['eb_data'].iloc[0]['correct'] / self.db['eb_data'].iloc[0]['total']
        else:
            new_word_id = self.db['new_words'].pop()
            entry = self.knowledge.loc[new_word_id]
            self.current_id = new_word_id
            stat['is_new'] = True

        stat['unseen_count'] = len(self.db['new_words'])
        return entry['word'], entry['pron'], entry['mean'], entry['syn'], entry['ex'], entry['note'], stat

    def eb_update_model(self, eb_df, correct):
        item_index = eb_df[eb_df['id'] == self.current_id].index[0]
        eb_df.loc[item_index, 'total'] += 1
        eb_df.loc[item_index, 'correct'] += 1 if correct else 0
        new_model = ebisu.updateRecall(
            prior=eb_df.loc[item_index, 'model'],
            successes=eb_df.loc[item_index, 'correct'],
            total=eb_df.loc[item_index, 'total'],
            tnow=_time_diff_to_hr(eb_df.loc[item_index, 't_last'], datetime.now())
        )
        eb_df.at[item_index, 'model'] = new_model  # Note: loc can't assign tuple to a cell
        self.db['eb_data'].loc[item_index, 't_last'] = datetime.now()

    def set_quiz_result(self, result, note_updated):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'later', 'trash', 'init']
        if result != 'init':
            self.knowledge.loc[self.current_id, 'note'] = note_updated

            eb_df = self.db['eb_data']

            if (eb_df['id'] == self.current_id).any():  # Word in EB Database
                if result == 'yes':
                    self.eb_update_model(eb_df, correct=True)
                elif result == 'no':
                    self.eb_update_model(eb_df, correct=False)
                elif result == 'later':
                    pass
                elif result == 'trash':
                    self.db['eb_data'].drop(eb_df.loc[eb_df['id'] == self.current_id].index, inplace=True)
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
