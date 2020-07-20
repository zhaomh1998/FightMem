import pickle
import os
import numbers
import shutil
import re
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
        self.void = set()  # Stores entries popped out of new_words set but not added to Newbie

    def get_eb_df(self, hide_sln=False):
        df_out = self.db['eb_data'].copy()
        df_out['HourPassed'] = df_out['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x), 2)
        )
        df_out['Model_A'] = df_out['model'].apply(lambda x: round(x[0], 2))
        df_out['Model_B'] = df_out['model'].apply(lambda x: round(x[1], 2))
        df_out['Model_T'] = df_out['model'].apply(lambda x: round(x[2], 2))
        df_out = df_out.merge(self.knowledge, how='inner', on='word')
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'score', 'HourPassed', 'Model_T', 'Model_A', 'Model_B']]
        else:
            return df_out[['word', 'score', 'mean', 'syn', 'HourPassed', 'Model_T', 'Model_A', 'Model_B', ]]

    def get_newbie_df(self, hide_sln=False):
        df_out = self.db['newbie_data'].copy()
        df_out['MinPassed'] = df_out['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x) * 60, 2)
        )
        df_out = df_out.merge(self.knowledge, how='inner', on='word')
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'score', 'MinPassed', 'correct']]
        else:
            return df_out[['word', 'score', 'mean', 'syn', 'MinPassed', 'correct']]

    def get_trash_df(self, hide_sln=False):
        old_words = self.knowledge.index.difference(self.knowledge.loc[self.db['new_words']].index)
        learning_words = pd.Index(self.db['eb_data']['id'].to_numpy()).union(self.db['newbie_data']['id'].to_numpy())
        df_out = self.knowledge.loc[old_words.difference(learning_words)].copy()
        df_out['id'] = df_out.index
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out.reset_index(drop=True)[['word', 'pron', 'id']]
        else:
            return df_out.reset_index(drop=True)[['word', 'pron', 'mean', 'syn', 'id']]

    def get_knowledge_df(self, hide_sln=False):
        df_out = self.knowledge.copy()
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'pron']]
        else:
            return df_out[['word', 'pron', 'mean', 'syn', 'ex']]

    def get_star_df(self, hide_sln=False):
        eb_db = self.db['eb_data']
        df_out = eb_db[eb_db['star'] == True].copy()
        df_out['HourPassed'] = df_out['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x), 2)
        )
        df_out['Model_A'] = df_out['model'].apply(lambda x: round(x[0], 2))
        df_out['Model_B'] = df_out['model'].apply(lambda x: round(x[1], 2))
        df_out['Model_T'] = df_out['model'].apply(lambda x: round(x[2], 2))
        df_out = df_out.merge(self.knowledge, how='inner', on='word')
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'score', 'HourPassed', 'Model_T', 'Model_A', 'Model_B']]
        else:
            return df_out[['word', 'score', 'mean', 'syn', 'HourPassed', 'Model_T', 'Model_A', 'Model_B', ]]

    def get_triangle_df(self, hide_sln=False):
        eb_db = self.db['eb_data']
        df_out = eb_db[eb_db['triangle'] == True].copy()
        df_out['HourPassed'] = df_out['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x), 2)
        )
        df_out['Model_A'] = df_out['model'].apply(lambda x: round(x[0], 2))
        df_out['Model_B'] = df_out['model'].apply(lambda x: round(x[1], 2))
        df_out['Model_T'] = df_out['model'].apply(lambda x: round(x[2], 2))
        df_out = df_out.merge(self.knowledge, how='inner', on='word')
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'score', 'HourPassed', 'Model_T', 'Model_A', 'Model_B']]
        else:
            return df_out[['word', 'score', 'mean', 'syn', 'HourPassed', 'Model_T', 'Model_A', 'Model_B', ]]

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

    def new_entry(self, db_name, entry_id, total=0, correct=0, start_model=EB_MODEL, star=False, triangle=False):
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
            'score': 1,
            'star': star,
            'triangle': triangle
        }, ignore_index=True)

    def get_next_quiz(self, review_mode):
        """ High level API to get next knowledge """
        assert isinstance(review_mode, str) and review_mode in ['Normal', 'Eb Table Only', 'Newbie Table Only',
                                                                'Starred', 'Triangled']
        self.refresh_db_prediction()  # Required -- this sorts DBs by score
        eb_db = self.db['eb_data']
        newbie_db = self.db['newbie_data']
        knowledge_str = None
        if review_mode == 'Normal':
            # First priority review EB
            # Second priority get Newbie into EB
            # Third priority get new words into Newbie
            if eb_db.shape[0] != 0 and eb_db.iloc[0]['score'] < self.db['eb_thresh']:
                knowledge_str = eb_db.iloc[0]['word']
            elif newbie_db.shape[0] != 0 and newbie_db.iloc[0]['score'] < self.db['newbie_thresh']:
                knowledge_str = newbie_db.iloc[0]['word']
            else:
                new_word_id = next(iter(self.db['new_words']))  # Hack: get first item without pop. get_knowledge will pop it
                knowledge_str = self.knowledge.at[new_word_id, 'word']
        elif review_mode == 'Eb Table Only':
            if eb_db.shape[0] != 0:
                knowledge_str = eb_db.iloc[0]['word']
            else:
                print('Nothing left in Eb Table! Used normal mode instead.')
                return self.get_next_quiz('Normal')
        elif review_mode == 'Newbie Table Only':
            if newbie_db.shape[0] != 0:
                knowledge_str = newbie_db.iloc[0]['word']
            else:
                print('Nothing left in Eb Table! Used normal mode instead.')
                return self.get_next_quiz('Normal')
        elif review_mode == 'Starred':
            starred = eb_db[eb_db['star'] == True]
            if starred.shape[0] != 0:
                knowledge_str = starred.iloc[0]['word']
            else:
                print('Nothing left in Eb Table! Used normal mode instead.')
                return self.get_next_quiz('Normal')
        elif review_mode == 'Triangled':
            triangled = eb_db[eb_db['triangle'] == True]
            if triangled.shape[0] != 0:
                knowledge_str = triangled.iloc[0]['word']
            else:
                print('Nothing left in Eb Table! Used normal mode instead.')
                return self.get_next_quiz('Normal')

        assert knowledge_str is not None
        return self.get_knowledge(knowledge_str)

    def get_knowledge(self, knowledge_str):
        """ Find knowledge_str, and return tuple of info presenting at frontend """
        stat = ''
        eb_db = self.db['eb_data']
        newbie_db = self.db['newbie_data']
        # Search in Eb
        if (eb_db['word'] == knowledge_str).any():
            entry_index = eb_db[eb_db['word'] == knowledge_str].index[0]
            self.current_id = eb_db.loc[entry_index, 'id']
            star = eb_db.loc[entry_index, 'star']
            triangle = eb_db.loc[entry_index, 'triangle']
            entry = self.knowledge.loc[self.current_id]
            stat += '[Eb]     Correct ' + str(eb_db.loc[entry_index, 'correct']) + '/' \
                    + str(eb_db.loc[entry_index, 'total']) + ' = ' \
                    + str(round(eb_db.loc[entry_index, 'correct'] * 100 / eb_db.loc[entry_index, 'total'], 2)) + '%\n'
        # Search in Newbie
        elif (newbie_db['word'] == knowledge_str).any():
            entry_index = newbie_db[newbie_db['word'] == knowledge_str].index[0]
            self.current_id = newbie_db.loc[entry_index, 'id']
            star = newbie_db.loc[entry_index, 'star']
            triangle = newbie_db.loc[entry_index, 'triangle']
            entry = self.knowledge.loc[self.current_id]
            stat += '[Newbie] Correct ' + str(newbie_db.loc[entry_index, 'correct']) + '/' \
                    + str(newbie_db.loc[entry_index, 'total']) + ' = ' \
                    + str(round(newbie_db.loc[entry_index, 'correct'] * 100 / newbie_db.loc[entry_index, 'total'], 2)) \
                    + '%\n'
        # Should be in new_words or trash
        else:
            word_id = self.knowledge[self.knowledge['word'] == knowledge_str].index[0]
            if word_id in self.db['new_words']:
                # Remove selected word from new_words list
                # Note: DB not saved until user answer this quiz -- so if user quits now this action will not be saved
                self.db['new_words'] = self.db['new_words'].union(self.void)
                self.void = set()
                self.db['new_words'].remove(word_id)
                self.void.add(word_id)
                stat += 'New Knowledge\t'
            else:
                stat += 'Trashed\t'
            entry = self.knowledge.loc[word_id]
            star = False
            triangle = False
            self.current_id = word_id

        # Sanity check
        assert isinstance(self.current_id, numbers.Integral)
        stat += '            Remaining: ' + str(len(self.db['new_words']))
        return entry['word'], entry['pron'], entry['mean'], entry['syn'], entry['ex'], \
               entry['note'], bool(star), bool(triangle), stat  # Cast np.bool_ star and triangle to Python

    def eb_update_model(self, eb_df, correct, star, triangle):
        item_index = eb_df[eb_df['id'] == self.current_id].index[0]
        eb_df.at[item_index, 'total'] += 1
        eb_df.at[item_index, 'correct'] += 1 if correct else 0
        new_model = ebisu.updateRecall(
            prior=eb_df.loc[item_index, 'model'],
            successes=eb_df.loc[item_index, 'correct'],
            total=eb_df.loc[item_index, 'total'],
            tnow=_time_diff_to_hr(eb_df.loc[item_index, 't_last'], datetime.now())
        )
        eb_df.at[item_index, 'model'] = new_model  # Note: loc can't assign tuple to a cell
        eb_df.at[item_index, 't_last'] = datetime.now()
        eb_df.at[item_index, 'star'] = star
        eb_df.at[item_index, 'triangle'] = triangle

    def set_quiz_result(self, result, note_updated, star, triangle):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'to_eb', 'trash', 'init']
        assert isinstance(star, bool)
        assert isinstance(triangle, bool)
        if result != 'init':
            self.knowledge.loc[self.current_id, 'note'] = note_updated
            if self.current_id in self.void:
                self.void.remove(self.current_id)

            eb_df = self.db['eb_data']
            newbie_df = self.db['newbie_data']
            if (eb_df['id'] == self.current_id).any():  # Word in EB Database
                if result == 'yes':
                    self.eb_update_model(eb_df, correct=True, star=star, triangle=triangle)
                elif result == 'no':
                    self.eb_update_model(eb_df, correct=False, star=star, triangle=triangle)
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
                    self.eb_update_model(newbie_df, correct=True, star=star, triangle=triangle)
                    correct = newbie_df.at[entry_index[0], 'correct']
                    # Add to EB Database if correct more than <_NEW_WORD_TO_DB_THRESHOLD> times
                    if correct > self.db['newbie2eb_thresh']:
                        newbie_df.drop(entry_index, inplace=True)
                        self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'no':
                    self.eb_update_model(newbie_df, correct=False, star=star, triangle=triangle)
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
        self.db['new_words'] = self.db['new_words'].union(self.void)
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
        # Beta 1.1 to beta 1.2
        if db['db_version'] == ('Beta', 1, 1):
            db['eb_data']['star'] = False
            db['eb_data']['triangle'] = False
            db['newbie_data']['star'] = False
            db['newbie_data']['triangle'] = False
            db['db_version'] = ('Beta', 1, 2)
            print("Database Updated [Beta V1.1] -> [Beta V1.2]")
        if db['db_version'] == ('Beta', 1, 2):
            print("Database is up-to-date [Beta V1.2]")

        return db
    else:
        raise RuntimeError("Database cannot be recognized by update utility!")
