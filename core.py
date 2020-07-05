import pickle
import os
import pandas as pd
from datetime import datetime, timedelta
import ebisu

# Model Parameters
_EB_MODEL = (3., 3., 0.5)
_EB_QUIZ_THRESH = 0.7
_NEWBIE_MODEL = (1.5, 1.5, 0.1)
_NEWBIE_QUIZ_THRESH = 0.9
_NEWBIE_TO_EB_THRESH = 3


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
                'newbie_data': pd.DataFrame(columns=['id', 'word', 'model', 'total', 'correct', 't_last', 'score']),
                'new_words': set(range(self.knowledge.shape[0]))
            }

        self.current_id = None

    def get_eb(self):
        df_display = self.db['eb_data'].copy()
        df_display['HourPassed'] = df_display['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x), 2)
        )
        df_display['Model_A'] = df_display['model'].apply(lambda x: round(x[0], 2))
        df_display['Model_B'] = df_display['model'].apply(lambda x: round(x[1], 2))
        df_display['Model_T'] = df_display['model'].apply(lambda x: round(x[2], 2))
        return df_display[['word', 'score', 'HourPassed', 'Model_A', 'Model_B', 'Model_T']]

    def get_new(self):
        df_display = self.db['newbie_data'].copy()
        df_display['MinPassed'] = df_display['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x) * 60, 2)
        )
        return df_display[['word', 'score', 'MinPassed', 'correct']]

    def refresh_db_prediction(self):
        for db_name in ['eb_data', 'newbie_data']:
            self.db[db_name] = self.db[db_name].apply(self.eb_update_score, axis=1)
            self.db[db_name].sort_values(by='score', ascending=True, inplace=True)
            self.db[db_name].reset_index(drop=True, inplace=True)

    def eb_update_score(self, entry):
        entry['score'] = round(ebisu.predictRecall(
            prior=entry['model'],
            tnow=_time_diff_to_hr(entry['t_last'], datetime.now()),
            exact=True
        ), 4)
        return entry

    def new_entry(self, db_name, entry_id, total=0, correct=0, start_model=_EB_MODEL):
        # db_name: eb_data or newbie_data
        assert isinstance(db_name, str)
        assert db_name in self.db.keys()
        data = self.knowledge.loc[entry_id].to_dict()
        self.db[db_name] = self.db[db_name].append({
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
        # First priority review EB
        # Second priority get Newbie into EB
        # Third priority get new words into Newbie
        eb_db = self.db['eb_data']
        new_db = self.db['newbie_data']
        if eb_db.shape[0] != 0 and eb_db.iloc[0]['score'] < _EB_QUIZ_THRESH:
            self.current_id = eb_db.iloc[0]['id']
            entry = self.knowledge.loc[self.current_id]
            stat['is_new'] = False
            stat['rate'] = eb_db.iloc[0]['correct'] / eb_db.iloc[0]['total']
        elif new_db.shape[0] != 0 and new_db.iloc[0]['score'] < _NEWBIE_QUIZ_THRESH:
            self.current_id = new_db.iloc[0]['id']
            entry = self.knowledge.loc[self.current_id]
            stat['is_new'] = False
            stat['rate'] = new_db.iloc[0]['correct'] / new_db.iloc[0]['total']
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
        eb_df.loc[item_index, 't_last'] = datetime.now()

    def set_quiz_result(self, result, note_updated):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'later', 'trash', 'init']
        if result != 'init':
            self.knowledge.loc[self.current_id, 'note'] = note_updated

            eb_df = self.db['eb_data']
            newbie_df = self.db['newbie_data']
            if (eb_df['id'] == self.current_id).any():  # Word in EB Database
                if result == 'yes':
                    self.eb_update_model(eb_df, correct=True)
                elif result == 'no':
                    self.eb_update_model(eb_df, correct=False)
                elif result == 'later':
                    # FIXME: This item will still be chosen for new word
                    pass
                elif result == 'trash':
                    eb_df.drop(eb_df.loc[eb_df['id'] == self.current_id].index, inplace=True)
                self.refresh_db_prediction()

            elif (newbie_df['id'] == self.current_id).any():  # Word in Newbie Database
                entry_index = newbie_df[newbie_df['id'] == self.current_id].index
                if result == 'yes':
                    self.eb_update_model(newbie_df, correct=True)
                    correct = newbie_df.at[entry_index[0], 'correct']
                    # Add to EB Database if correct more than <_NEW_WORD_TO_DB_THRESHOLD> times
                    if correct > _NEWBIE_TO_EB_THRESH:
                        newbie_df.drop(entry_index, inplace=True)
                        self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'no':
                    self.eb_update_model(newbie_df, correct=False)
                    correct = newbie_df.at[entry_index[0], 'correct']
                    # Punish as wrong answer provided: correct - 1
                    if correct > 0:
                        newbie_df.at[entry_index[0], 'correct'] -= 1
                elif result == 'later':
                    # FIXME: This item will still be chosen for new word
                    pass
                elif result == 'trash':
                    newbie_df.drop(entry_index, inplace=True)
                self.refresh_db_prediction()

            else:  # Add to Newbie Word Database
                if result == 'yes':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=1, start_model=_NEWBIE_MODEL)
                elif result == 'no':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=0, start_model=_NEWBIE_MODEL)
                elif result == 'later':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=1, start_model=_NEWBIE_MODEL)
                elif result == 'trash':
                    pass  # Does not add to review list

            self.save()

    def save(self):
        pickle.dump(self.knowledge, open(self.knowledge_path, 'wb'))
        pickle.dump(self.db, open(self.db_path, 'wb'))


def _time_diff_to_hr(time_a, time_b):
    one_hour = timedelta(hours=1)
    return abs((time_a - time_b) / one_hour)
