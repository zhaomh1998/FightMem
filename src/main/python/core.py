import pickle
import os
import numbers
import shutil
import re
import time
from datetime import datetime, timedelta
import pandas as pd
import ebisu
from df2gspread import df2gspread as d2g
from parameter import EB_MODEL, EB_QUIZ_THRESH_DEFAULT, \
    NEWBIE_MODEL, NEWBIE_QUIZ_THRESH_DEFAULT, NEWBIE_TO_EB_THRESH_DEFAULT, NEWBIE_RETEST_SCHEDULE, LONG_MODEL, \
    HP_FULL, HP_AWARD_EB, HP_AWARD_NEWBIE, HP_AWARD_NEW, HARD_PUNISH_MULTIPLIER


class FightMem:
    def __init__(self, data_fold_path, knowledge_file, database_file=None):
        assert os.path.exists(data_fold_path), '\'data\' folder not found!'
        self.knowledge_path = os.path.join(data_fold_path, knowledge_file)
        backup_fold = os.path.join(data_fold_path, 'bak')
        if not os.path.exists(backup_fold):
            os.mkdir(backup_fold)

        assert os.path.exists(self.knowledge_path), f'Cannot locate <{knowledge_file}>. Please check!'
        now = datetime.now()
        bak_extension = '_' + now.strftime('%m_%d_%Y__%H_%M_%S') + '.bak'
        shutil.copyfile(self.knowledge_path, os.path.join(backup_fold, knowledge_file) + bak_extension)
        self.knowledge = pickle.load(open(self.knowledge_path, 'rb'))
        assert isinstance(self.knowledge, pd.DataFrame)

        if database_file is None:
            database_file = os.path.splitext(knowledge_file)[0] + '.fmdb'

        self.db_path = os.path.join(data_fold_path, database_file)
        if os.path.exists(self.db_path):
            shutil.copyfile(self.db_path, os.path.join(backup_fold, database_file) + bak_extension)
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
            pickle.dump(self.db, open(self.db_path, 'wb'))
            self.db = _load_update_db(self.db_path)

        self.current_id = None
        self.void = set()  # Stores entries popped out of new_words set but not added to Newbie
        self.hp = HP_FULL
        self.hp_t = time.time()

    def get_learn_df(self, hide_sln=False, hide_high_score=False):
        eb_thresh = self.db['eb_thresh'] if hide_high_score else 1
        newbie_thresh = self.db['newbie_thresh'] if hide_high_score else 1
        df_eb = self.db['eb_data'].copy()
        df_eb = df_eb[df_eb['score'] <= eb_thresh].sort_values('score', ignore_index=True)
        df_eb['Table'] = 'Eb'
        df_newbie = self.db['newbie_data'].copy()
        df_newbie = df_newbie[df_newbie['score'] <= newbie_thresh].sort_values('score', ignore_index=True)
        df_newbie['Table'] = 'Newbie'
        df_out = pd.concat([df_eb, df_newbie], ignore_index=True)
        df_out['yes'] = 'O'
        df_out['no'] = 'X'
        df_out['trash'] = '🗑'
        df_out['HourPassed'] = df_out['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x), 2)
        )
        df_out = df_out.merge(self.knowledge, how='inner', on='word')
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'yes', 'no', 'trash', 'HourPassed', 'Table']]
        else:
            return df_out[['word', 'yes', 'no', 'trash', 'HourPassed', 'note', 'mean', 'syn', 'Table']]

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
            return df_out[['word', 'score', 'HourPassed', 'Model_T', 'Model_A', 'Model_B', 'bury', 'bury_t']]
        else:
            return df_out[['word', 'score', 'mean', 'syn', 'HourPassed', 'Model_T', 'Model_A', 'Model_B', 'bury', 'bury_t']]

    def get_newbie_df(self, hide_sln=False):
        df_out = self.db['newbie_data'].copy()
        df_out['MinPassed'] = df_out['t_last'].apply(
            lambda x: round(_time_diff_to_hr(datetime.now(), x) * 60, 2)
        )
        df_out = df_out.merge(self.knowledge, how='inner', on='word')
        # Extract out Chinese characters for meaning
        df_out['mean'] = df_out['mean'].apply(lambda x: ' '.join(re.findall(r'([\u4e00-\u9fa5]+)', x)))
        if hide_sln:
            return df_out[['word', 'score', 'MinPassed', 'NextReview', 'correct']]
        else:
            return df_out[['word', 'score', 'mean', 'syn', 'MinPassed', 'NextReview', 'correct']]

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
        return version_str, self.db['eb_thresh'], self.db['newbie_thresh'], self.db['newbie2eb_thresh'], \
            self.db['gsheet_id']

    def set_setting(self, eb_thresh=None, newbie_thresh=None, newbie2eb_thresh=None, gsheet_id=None):
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
        if gsheet_id is not None:
            print(f'Updating gsheet id to >{gsheet_id}<')
            assert isinstance(gsheet_id, str)
            self.db['gsheet_id'] = gsheet_id

    def refresh_db_prediction(self):
        for db_name in ['eb_data', 'newbie_data']:
            if self.db[db_name].shape[0] != 0:
                self.db[db_name] = self.db[db_name].apply(self.eb_update_score, axis=1)

        if self.db['eb_data'].shape[0] != 0:
            self.db['eb_data'].sort_values(by='score', ascending=True, inplace=True, ignore_index=True)
            self.db['eb_data']['bury'] = self.db['eb_data']['bury_t'].apply(lambda x: x.date() == datetime.today().date())

        if self.db['newbie_data'].shape[0] != 0:
            self.db['newbie_data']['NextReview'] = self.db['newbie_data']['t_last'].apply(
                lambda x: round(_time_diff_to_hr(datetime.now(), x) * 60, 2)
            )
            self.db['newbie_data']['NextReview'] = self.db['newbie_data']['t_last'].apply(
                lambda x: round(_time_diff_to_hr(datetime.now(), x) * 60, 2)
            )
            self.db['newbie_data']['NextReview'] = self.db['newbie_data']['correct'].apply(NEWBIE_RETEST_SCHEDULE) \
                - self.db['newbie_data']['NextReview']
            self.db['newbie_data'].sort_values(by='NextReview', ascending=True, inplace=True, ignore_index=True)

    def eb_update_score(self, entry):
        entry['score'] = round(ebisu.predictRecall(
            prior=entry['model'],
            tnow=_time_diff_to_hr(entry['t_last'], datetime.now()),
            exact=True
        ), 4)
        return entry

    def new_entry(self, db_name, entry_id, total=0, correct=0, start_model=EB_MODEL, star=False, triangle=False,
                  bury=False):
        # db_name: eb_data or newbie_data
        if not bury:
            bury_t = datetime(year=1970, month=1, day=1)
        else:
            bury_t = datetime.now()
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
            'triangle': triangle,
            'bury_t': bury_t,
            'bury': False
        }, ignore_index=True)

    def get_next_quiz(self, review_mode):
        """ High level API to get next knowledge """
        assert isinstance(review_mode, str) and review_mode in ['Normal', 'Eb Table Only', 'Newbie Table Only',
                                                                'Starred', 'Triangled']
        self.refresh_db_prediction()  # Required -- this sorts DBs by score
        eb_db = self.db['eb_data']
        eb_db = eb_db[eb_db['bury'] == False]
        newbie_db = self.db['newbie_data']
        knowledge_str = None
        if review_mode == 'Normal':
            # First priority review EB
            # Second priority get Newbie into EB
            # Third priority get new words into Newbie
            if eb_db.shape[0] != 0 and eb_db.iloc[0]['score'] < self.db['eb_thresh']:
                knowledge_str = eb_db.iloc[0]['word']
            elif newbie_db.shape[0] != 0 and newbie_db.iloc[0]['NextReview'] < 0:
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
            stat += f'            HL: ' + str(round(eb_db.loc[entry_index, 'model'][2], 2)) + '\n'
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
        review_cnt = self.db['eb_data'][self.db['eb_data']['score'] < self.db['eb_thresh']].count().iloc[0]
        stat += '            Remaining: N ' + str(len(self.db['new_words'])) + ', R ' + str(review_cnt)

        return entry['word'], entry['pron'], entry['mean'], entry['syn'], entry['ex'], \
               entry['note'], bool(star), bool(triangle), stat  # Cast np.bool_ star and triangle to Python

    def eb_update_model(self, eb_df, correct, star, triangle, overwrite_model=None, bury=False, hl_modify=1):
        item_index = eb_df[eb_df['id'] == self.current_id].index[0]
        eb_df.at[item_index, 'total'] += 1
        eb_df.at[item_index, 'correct'] += 1 if correct else 0
        if overwrite_model is None:
            try:
                new_model = ebisu.updateRecall(
                    prior=eb_df.loc[item_index, 'model'],
                    successes=eb_df.loc[item_index, 'correct'],
                    total=eb_df.loc[item_index, 'total'],
                    tnow=_time_diff_to_hr(eb_df.loc[item_index, 't_last'], datetime.now())
                )
                # For 'hard' response punishment
                new_model = (new_model[0], new_model[1], new_model[2] / hl_modify)
            except AssertionError as e:
                print('Ebisu model was very surprised with the result!')
                print(e)
                print('Resetting the model')
                new_model = EB_MODEL
                eb_df.at[item_index, 'total'] = 1
                eb_df.at[item_index, 'correct'] = 1
        else:
            assert isinstance(overwrite_model, tuple) and len(overwrite_model) == 3
            new_model = overwrite_model
        eb_df.at[item_index, 'model'] = new_model  # Note: loc can't assign tuple to a cell
        eb_df.at[item_index, 't_last'] = datetime.now()
        eb_df.at[item_index, 'star'] = star
        eb_df.at[item_index, 'triangle'] = triangle
        if bury:
            eb_df.at[item_index, 'bury_t'] = datetime.now()

    def set_quiz_result(self, result, note_updated, star, triangle):
        """ High level API to set quiz result """
        assert result in ['yes', 'no', 'to_eb', 'trash', 'init', 'long', 'bury', 'hard']
        assert isinstance(star, bool)
        assert isinstance(triangle, bool)
        if result != 'init':
            self.knowledge.loc[self.current_id, 'note'] = note_updated
            if self.current_id in self.void:
                self.void.remove(self.current_id)

            eb_df = self.db['eb_data']
            newbie_df = self.db['newbie_data']
            hp_award = 0
            if (eb_df['id'] == self.current_id).any():  # Word in EB Database
                hp_award = HP_AWARD_EB
                if result == 'yes':
                    self.eb_update_model(eb_df, correct=True, star=star, triangle=triangle)
                elif result == 'no':
                    self.eb_update_model(eb_df, correct=False, star=star, triangle=triangle)
                elif result == 'hard':
                    self.eb_update_model(eb_df, correct=False, star=star, triangle=triangle,
                                         hl_modify=HARD_PUNISH_MULTIPLIER)
                elif result == 'to_eb':
                    # No action taken -- Already in eb
                    # TODO: Make it ToNew instead
                    pass
                elif result == 'trash':
                    eb_df.drop(eb_df.loc[eb_df['id'] == self.current_id].index, inplace=True)
                elif result == 'long':
                    self.eb_update_model(eb_df, correct=True, star=star, triangle=triangle, overwrite_model=LONG_MODEL)
                elif result == 'bury':
                    self.eb_update_model(eb_df, correct=True, star=star, triangle=triangle, bury=True)
                self.refresh_db_prediction()

            elif (newbie_df['id'] == self.current_id).any():  # Word in Newbie Database
                hp_award = HP_AWARD_NEWBIE
                entry_index = newbie_df[newbie_df['id'] == self.current_id].index
                if result == 'yes':
                    self.eb_update_model(newbie_df, correct=True, star=star, triangle=triangle)
                    correct = newbie_df.at[entry_index[0], 'correct']
                    # Add to EB Database if correct more than <_NEW_WORD_TO_DB_THRESHOLD> times
                    if correct > self.db['newbie2eb_thresh']:
                        newbie_df.drop(entry_index, inplace=True)
                        self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'no' or result == 'hard':
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
                elif result == 'long':
                    newbie_df.drop(entry_index, inplace=True)
                    self.new_entry('eb_data', self.current_id, total=1, correct=1, start_model=LONG_MODEL)
                elif result == 'bury':
                    newbie_df.drop(entry_index, inplace=True)
                    self.new_entry('eb_data', self.current_id, total=1, correct=1, bury=True)
                self.refresh_db_prediction()

            else:  # Add to Newbie Word Database
                hp_award = HP_AWARD_NEW
                if result == 'yes':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=1, start_model=NEWBIE_MODEL)
                elif result == 'no' or result == 'hard':
                    self.new_entry('newbie_data', self.current_id, total=1, correct=0, start_model=NEWBIE_MODEL)
                elif result == 'to_eb':
                    self.new_entry('eb_data', self.current_id, total=1, correct=1)
                elif result == 'trash':
                    pass  # Does not add to review list
                elif result == 'long':
                    self.new_entry('eb_data', self.current_id, total=1, correct=1, start_model=LONG_MODEL)
                elif result == 'bury':
                    self.new_entry('eb_data', self.current_id, total=1, correct=1, bury=True)
            self.save()

            # Update HP bar with reward
            # No threading involved for HP bar update so shouldn't have race condition?
            # NOTE: +1 so that it can be displayed as full for some time
            self.hp = min(self.get_hp() + hp_award, HP_FULL + 1)
            self.hp_t = time.time()

    def save(self):
        self.db['new_words'] = self.db['new_words'].union(self.void)
        pickle.dump(self.knowledge, open(self.knowledge_path, 'wb'))
        pickle.dump(self.db, open(self.db_path, 'wb'))

    def sync_gs(self):
        assert len(self.db['gsheet_id']) != 0, 'Google Sheet ID cannot be empty! Please find the sheet id from link:' \
                                               'https://docs.google.com/spreadsheets/d/<sheet id>/edit'
        print('Uploading Eb...')
        d2g.upload(self.get_eb_df(), self.db['gsheet_id'], 'Eb')
        print('Uploading Learn...')
        d2g.upload(self.get_learn_df(), self.db['gsheet_id'], 'Learn')
        print('Uploading Newbie...')
        d2g.upload(self.get_newbie_df(), self.db['gsheet_id'], 'Newbie')
        print('Uploading Star...')
        d2g.upload(self.get_star_df(), self.db['gsheet_id'], 'Star')
        print('Uploading Triangle...')
        d2g.upload(self.get_triangle_df(), self.db['gsheet_id'], 'Triangle')
        print('Uploading All...')
        d2g.upload(self.get_knowledge_df(), self.db['gsheet_id'], 'All')
        print('Google Sheet Sync completed!')

    def get_hp(self):
        return max(0, int(self.hp - (time.time() - self.hp_t)))


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
        # Beta 1.2 to beta 1.3
        if db['db_version'] == ('Beta', 1, 2):
            db['gsheet_id'] = ''
            db['db_version'] = ('Beta', 1, 3)
            print("Database Updated [Beta V1.2] -> [Beta V1.3]")
        # Beta 1.3 to beta 1.4
        if db['db_version'] == ('Beta', 1, 3):
            db['eb_data']['bury_t'] = datetime(year=1970, month=1, day=1)
            db['eb_data']['bury'] = False
            db['newbie_data']['bury_t'] = datetime(year=1970, month=1, day=1)
            db['newbie_data']['bury'] = False
            db['db_version'] = ('Beta', 1, 4)
            print("Database Updated [Beta V1.3] -> [Beta V1.4]")
        if db['db_version'] == ('Beta', 1, 4):
            print("Database is up-to-date [Beta V1.4]")

        return db
    else:
        raise RuntimeError("Database cannot be recognized by update utility!")
