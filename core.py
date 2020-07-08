import pickle
import os
import numbers
import shutil
import pandas as pd
from datetime import datetime, timedelta
import ebisu
from parameter import EB_MODEL, EB_QUIZ_THRESH_DEFAULT, \
    NEWBIE_MODEL, NEWBIE_QUIZ_THRESH_DEFAULT, NEWBIE_TO_EB_THRESH_DEFAULT


class FightMem:
    def __init__(self, knowledge_file, database_file=None):
        assert os.path.exists(knowledge_file), f'Cannot locate <{knowledge_file}>. Please check!'
        self.knowledge_path = knowledge_file
        now = datetime.now()
        bak_extension = '_' + now.strftime('%m_%d_%Y__%H_%M_%S') + '.bak'
        shutil.copyfile(self.knowledge_path, self.knowledge_path + bak_extension)
        self.knowledge = pickle.load(open(knowledge_file, 'rb'))
        assert isinstance(self.knowledge, pd.DataFrame)

        if database_file is None:
            self.db_path = os.path.splitext(knowledge_file)[0] + '.fmdb'
        else:
            self.db_path = database_file
        if os.path.exists(self.db_path):
            shutil.copyfile(self.db_path, self.db_path + bak_extension)
            self.db = _load_update_db(self.db_path)
        else:
            self.db = {
                'eb_data': pd.DataFrame(columns=['id', 'word', 'model', 'total', 'correct', 't_last', 'score']),
                'newbie_data': pd.DataFrame(columns=['id', 'word', 'model', 'total', 'correct', 't_last', 'score']),
                'new_words': set(range(self.knowledge.shape[0])),
                'eb_thresh': EB_QUIZ_THRESH_DEFAULT,
                'newbie_thresh': NEWBIE_QUIZ_THRESH_DEFAULT,
                'newbie2eb_thresh': NEWBIE_TO_EB_THRESH_DEFAULT,
                'db_version': ('Beta', 1, 1)
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

    def get_setting(self):
        version = self.db['db_version']
        version_str = f"{version[0]} V{version[1]}.{version[2]}"
        return version_str, self.db['eb_thresh'], self.db['newbie_thresh'], self.db['newbie2eb_thresh']

    def set_setting(self, eb_thresh=None, newbie_thresh=None, newbie2eb_thresh=None):
        if eb_thresh is not None:
            assert isinstance(eb_thresh, float)
            assert 0 < eb_thresh < 1
            self.db['eb_thresh'] = round(eb_thresh, 2)
        if newbie_thresh is not None:
            assert isinstance(newbie_thresh, float)
            assert 0 < newbie_thresh < 1
            self.db['newbie_thresh'] = round(newbie_thresh, 2)
        if newbie2eb_thresh is not None:
            assert isinstance(newbie2eb_thresh, int)
            assert newbie2eb_thresh > 0
            self.db['newbie2eb_thresh'] = newbie2eb_thresh

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

    def new_entry(self, db_name, entry_id, total=0, correct=0, start_model=EB_MODEL):
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
        stat = ''
        # First priority review EB
        # Second priority get Newbie into EB
        # Third priority get new words into Newbie
        eb_db = self.db['eb_data']
        new_db = self.db['newbie_data']
        # TODO: Refactor to which entry to test
        if eb_db.shape[0] != 0 and eb_db.iloc[0]['score'] < self.db['eb_thresh']:
            self.current_id = eb_db.iloc[0]['id']
            entry = self.knowledge.loc[self.current_id]
            stat += '[Eb]     Correct ' + str(eb_db.iloc[0]['correct']) + '/' \
                    + str(eb_db.iloc[0]['total']) + ' = ' + \
                    str(round(eb_db.iloc[0]['correct'] * 100 / eb_db.iloc[0]['total'], 2)) + '%\n'
        elif new_db.shape[0] != 0 and new_db.iloc[0]['score'] < self.db['newbie_thresh']:
            self.current_id = new_db.iloc[0]['id']
            entry = self.knowledge.loc[self.current_id]
            stat += '[Newbie] Correct ' + str(new_db.iloc[0]['correct']) + '/' \
                    + str(new_db.iloc[0]['total']) + ' = ' + \
                    str(round(new_db.iloc[0]['correct'] * 100 / new_db.iloc[0]['total'], 2)) + '%\n'
        else:
            new_word_id = self.db['new_words'].pop()
            entry = self.knowledge.loc[new_word_id]
            self.current_id = new_word_id
            stat += 'New Knowledge\t'

        assert isinstance(self.current_id, numbers.Integral)
        stat += '            Remaining: ' + str(len(self.db['new_words']))
        return entry['word'], entry['pron'], entry['mean'], entry['syn'], entry['ex'], entry['note'], stat

    def get_knowledge(self, knowledge_str):
        """ High level API to get a specific knowledge """
        entry = self.knowledge[self.knowledge['word'] == knowledge_str].iloc[0]
        self.current_id = entry.name
        stat = ''
        stat += '            Remaining: ' + str(len(self.db['new_words']))
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
        assert result in ['yes', 'no', 'to_eb', 'trash', 'init']
        if result != 'init':
            self.knowledge.loc[self.current_id, 'note'] = note_updated

            eb_df = self.db['eb_data']
            newbie_df = self.db['newbie_data']
            if (eb_df['id'] == self.current_id).any():  # Word in EB Database
                if result == 'yes':
                    self.eb_update_model(eb_df, correct=True)
                elif result == 'no':
                    self.eb_update_model(eb_df, correct=False)
                elif result == 'to_eb':
                    # No action taken -- Already in eb
                    # TODO: Make it ToNew instead
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
                    if correct > self.db['newbie2eb_thresh']:
                        newbie_df.drop(entry_index, inplace=True)
                        self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'no':
                    self.eb_update_model(newbie_df, correct=False)
                    correct = newbie_df.at[entry_index[0], 'correct']
                    # Punish as wrong answer provided: correct - 1
                    if correct > 0:
                        newbie_df.at[entry_index[0], 'correct'] -= 1
                elif result == 'to_eb':
                    newbie_df.drop(entry_index, inplace=True)
                    self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'trash':
                    newbie_df.drop(entry_index, inplace=True)
                self.refresh_db_prediction()

            else:  # Add to Newbie Word Database
                if result == 'yes':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=1, start_model=NEWBIE_MODEL)
                elif result == 'no':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=0, start_model=NEWBIE_MODEL)
                elif result == 'to_eb':
                    self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'trash':
                    pass  # Does not add to review list

            self.save()

    def save(self):
        pickle.dump(self.knowledge, open(self.knowledge_path, 'wb'))
        pickle.dump(self.db, open(self.db_path, 'wb'))


def _time_diff_to_hr(time_a, time_b):
    one_hour = timedelta(hours=1)
    return abs((time_a - time_b) / one_hour)


def _load_update_db(path):
    assert os.path.exists(path)
    db = pickle.load(open(path, 'rb'))
    if isinstance(db, dict):
        # Beta 1.0 to beta 1.1
        if sorted(db.keys()) == ['eb_data', 'new_words', 'newbie_data']:
            db['eb_thresh'] = EB_QUIZ_THRESH_DEFAULT
            db['newbie_thresh'] = NEWBIE_QUIZ_THRESH_DEFAULT
            db['newbie2eb_thresh'] = NEWBIE_TO_EB_THRESH_DEFAULT
            db['db_version'] = ('Beta', 1, 1)
            print("Database Updated [Beta V1.0] -> [Beta V1.1]")
        elif db['db_version'] == ('Beta', 1, 1):
            print("Database is up-to-date [Beta V1.1]")
        else:
            raise RuntimeError("Database cannot be recognized by update utility!")

        return db
    else:
        raise RuntimeError("Database cannot be recognized by update utility!")
