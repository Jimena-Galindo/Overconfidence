

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
import seaborn as sns

# Read in the data from the ego treatment sessions
# import the data in wide format for each session
session1 = pd.read_csv("Data/session1_ego.csv")
session2 = pd.read_csv("Data/session2_ego.csv")
session3 = pd.read_csv("Data/session3_ego.csv")
session4 = pd.read_csv("Data/session4_ego.csv")

# concatenate the sessions
ego_wide = pd.concat([session1, session2, session3, session4], axis=0, sort=False)

ego_wide['treatment'] = 'ego'
ego_wide.reset_index(inplace=True)

######## Read in the data from the stereotype treatment sessions
# import the data in wide format
stereo_wide = pd.read_csv("Simulations/demo/data/stereo_demo_data.csv")
stereo_wide['treatment'] = 'stereotype'

# from the data frame ego_wide, select all the columns that have names that start with 'Quizzes' and append the column 'participant.code
quiz_cols = [col for col in ego_wide.columns if 'Quizzes' in col]+['participant.code', 'treatment']


# from the data frame ego_wide, select all the columns that have names that start with 'participant.'
participant_cols = [col for col in ego_wide.columns if 'participant' in col]+['participant.code']

# from the data frame ego_wide, select all the columns that have names that start with 'session.'
session_cols = [col for col in ego_wide.columns if 'session' in col]+['participant.code']

# from the data frame ego_wide, select all the columns that have names that start with 'Signals.'
signal_cols = [col for col in ego_wide.columns if 'Signals' in col]+['participant.code']

# from the data frame ego_wide, select all the columns that have names that start with 'SignalsOther.'
signal_other_cols = [col for col in ego_wide.columns if 'SignalsOther' in col]+['participant.code']

# from the data frame ego_wide, select all the columns that have names that start with 'Questionnaire.'
questionnaire_cols = [col for col in ego_wide.columns if 'Questionnaire' in col]+['participant.code']

# split the data frame ego_wide into 6 data frames using the columns we just selected
ego_quiz = ego_wide[quiz_cols]
ego_participant = ego_wide[participant_cols]
ego_session = ego_wide[session_cols]
ego_signal = ego_wide[signal_cols]
ego_signal_other = ego_wide[signal_other_cols] # this has no information for the ego treatment
ego_questionnaire = ego_wide[questionnaire_cols]

# for ego_quiz rename all the columns to remove the prefix 'Quizzes'
ego_quiz.columns = [col.replace('Quizzes.','') for col in ego_quiz.columns]
# for ego_quiz rename all the columns to remove the prefix 'player'
ego_quiz.columns = [col.replace('player.','') for col in ego_quiz.columns]
# drop all the columns that have either 'group.' or 'subsession.' in the name
ego_quiz = ego_quiz[[col for col in ego_quiz.columns if 'group.' not in col and 'subsession.' not in col]]
# melt the data making the participant code the id variable
ego_quiz_long = pd.melt(ego_quiz, id_vars=['participant.code'])
# split the variable column into two columns, one for the round_number and one for the question
ego_quiz_long[['round_number','variable_name']] = ego_quiz_long['variable'].str.split('.', expand=True)
# drop the column variable with the long names
ego_quiz_long = ego_quiz_long.drop('variable', axis=1)
# reshape ego_quiz_long from long to wide format by making each of the values in variable_name a column
ego_quiz_wide = ego_quiz_long.pivot(index=['participant.code','round_number'], columns=['variable_name'], values='value')
# make a table that has only the score for each topic and the participant code
ego_scores = ego_quiz_wide[['topic', 'score']]
# reset the index so that participant_code is just another colum
ego_scores.reset_index(inplace=True)

# rename all the other variables withoutht the 'participant.' prefix
ego_participant.columns = [col.replace('participant.','') for col in ego_participant.columns]

# from ego_signal drop all the columns that have the 'SignalsOther.' prefix
ego_signal = ego_signal[[col for col in ego_signal.columns if 'SignalsOther.' not in col]]

# remove the 'Signals.' prefix from all the column names and the 'participant.' prefix from the code column
ego_signal.columns = [col.replace('Signals.','') for col in ego_signal.columns]
ego_signal.columns = [col.replace('participant.','') for col in ego_signal.columns]
# replace the 'player.' in the names of the columns
ego_signal.columns = [col.replace('player.', '') for col in ego_signal.columns]

# drop the group and subsession level columns
ego_signal = ego_signal[[col for col in ego_signal.columns if 'group.' not in col and '.subsession' not in col]]

# melt the data set making code the id column. then split all the variable names
ego_signal_long = pd.melt(ego_signal, id_vars='code')

# split the variable column into two columns, one for the round_number and one for the question
ego_signal_long[['round_number','variable_name']] = ego_signal_long['variable'].str.split('.', expand=True)
# drop the column variable with the long names
ego_signal_long = ego_signal_long.drop('variable', axis=1)

# reshape ego_signal_long from long to wide format by making each of the values in variable_name a column
ego_signal_wide = ego_signal_long.pivot(index=['code','round_number'], columns=['variable_name'], values='value')
ego_signal_wide.reset_index(inplace=True)

beliefs = ego_signal_wide.loc[ego_signal_wide['science_belief']>=0, 
                    ['code','science_belief', 'us_belief', 'math_belief', 'verbal_belief', 'pop_belief', 'sports_belief',
                    'science_certainty', 'us_certainty', 'math_certainty', 'verbal_certainty', 'pop_certainty', 'sports_certainty']]

# the round_numbers range from 1 to 60. I want all of them to range from 1 to 11 by setting 11 to 1, 21 to 1, 12 to 2, etc.
ego_signal_wide['round_number'] = ego_signal_wide['round_number'].astype(int)

ego_signal_wide['round_number'].replace([12,23,34,45,56], 1, inplace=True)
ego_signal_wide['round_number'].replace([13,24,35,46,57], 2, inplace=True)
ego_signal_wide['round_number'].replace([14,25,36,47,58], 3, inplace=True)
ego_signal_wide['round_number'].replace([15,26,37,48,59], 4, inplace=True)
ego_signal_wide['round_number'].replace([16,27,38,49,60], 5, inplace=True)
ego_signal_wide['round_number'].replace([17,28,39,50,61], 6, inplace=True)
ego_signal_wide['round_number'].replace([18,29,40,51,62], 7, inplace=True)
ego_signal_wide['round_number'].replace([19,30,41,52,63], 8, inplace=True)
ego_signal_wide['round_number'].replace([20,31,42,53,64], 9, inplace=True)
ego_signal_wide['round_number'].replace([21,32,43,54,65], 10, inplace=True)
ego_signal_wide['round_number'].replace([22,33,44,55,66], 11, inplace=True)

# split the data by topic
ego_science = ego_signal_wide.loc[(ego_signal_wide['effort']>=0) & (ego_signal_wide['topic']=='Science and Technology'), 
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'science_score', 'topic', 'signal']]
# impute the values for science_belief and the science_certainty from the table beliefs
ego_science = ego_science.merge(beliefs[['code', 'science_belief', 'science_certainty']], on='code', how='left')

# add a column with the type according to the science score
ego_science.loc[ego_science['science_score']>15, 'type'] = '2'
ego_science.loc[ego_science['science_score']<=15, 'type'] = '1'
ego_science.loc[ego_science['science_score']<6, 'type'] = '0'

# make a data frame for math exactly as ego_science but with the math score and belief
ego_math = ego_signal_wide.loc[(ego_signal_wide['effort']>=0) & (ego_signal_wide['topic']=='Math'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'math_score', 'topic', 'signal']]
# impute the values for math_belief and the math_certainty from the table beliefs
ego_math = ego_math.merge(beliefs[['code', 'math_belief', 'math_certainty']], on='code', how='left')

# add a column with the type according to the science score
ego_math.loc[ego_math['math_score']>15, 'type'] = '2'
ego_math.loc[ego_math['math_score']<=15, 'type'] = '1'
ego_math.loc[ego_math['math_score']<6, 'type'] = '0'

# make a data frame for verbal exactly as ego_science but with the verbal score and belief
ego_verbal = ego_signal_wide.loc[(ego_signal_wide['effort']>=0) & (ego_signal_wide['topic']=='Verbal'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'verbal_score', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
ego_verbal = ego_verbal.merge(beliefs[['code', 'verbal_belief', 'verbal_certainty']], on='code', how='left')

# add a column with the type according to the science score
ego_verbal.loc[ego_verbal['verbal_score']>15, 'type'] = '2'
ego_verbal.loc[ego_verbal['verbal_score']<=15, 'type'] = '1'
ego_verbal.loc[ego_verbal['verbal_score']<6, 'type'] = '0'

# make a data frame for verbal exactly as ego_science but with the verbal score and belief
ego_pop = ego_signal_wide.loc[(ego_signal_wide['effort']>=0) & (ego_signal_wide['topic']=='Pop-Culture and Art'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'pop_score', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
ego_pop = ego_pop.merge(beliefs[['code', 'pop_belief', 'pop_certainty']], on='code', how='left')

# add a column with the type according to the science score
ego_pop.loc[ego_pop['pop_score']>15, 'type'] = '2'
ego_pop.loc[ego_pop['pop_score']<=15, 'type'] = '1'
ego_pop.loc[ego_pop['pop_score']<6, 'type'] = '0'

# make a data frame for verbal exactly as ego_science but with the verbal score and belief
ego_sports = ego_signal_wide.loc[(ego_signal_wide['effort']>=0) & (ego_signal_wide['topic']=='Sports and Video Games'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'sports_score', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
ego_sports = ego_sports.merge(beliefs[['code', 'sports_belief', 'sports_certainty']], on='code', how='left')

# add a column with the type according to the science score
ego_sports.loc[ego_sports['sports_score']>15, 'type'] = '2'
ego_sports.loc[ego_sports['sports_score']<=15, 'type'] = '1'
ego_sports.loc[ego_sports['sports_score']<6, 'type'] = '0'

# make a data frame for verbal exactly as ego_science but with the verbal score and belief
ego_us = ego_signal_wide.loc[(ego_signal_wide['effort']>=0) & (ego_signal_wide['topic']=='US Geography'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'us_score', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
ego_us = ego_us.merge(beliefs[['code', 'us_belief', 'us_certainty']], on='code', how='left')

# add a column with the type according to the science score
ego_us.loc[ego_us['us_score']>15, 'type'] = '2'
ego_us.loc[ego_us['us_score']<=15, 'type'] = '1'
ego_us.loc[ego_us['us_score']<6, 'type'] = '0'

# from the ego session data frame select only the columns that we will use
ego_session = ego_session[['participant.id_in_session', 
                            'session.code', 
                            'session.w_verbal', 
                            'session.w_math', 
                            'session.w_pop',
                            'session.w_science',
                            'session.w_sports',
                            'session.w_us']]

# in ego_session remove the prefixes 'participant.' and 'session.' from the column names
ego_session.columns = [col.replace('participant.','') for col in ego_session.columns]
ego_session.columns = [col.replace('session.','') for col in ego_session.columns]
# add a column to each of the topics tables with the corresponding value of w from the ego_session table
ego_science['rate']=ego_session['w_science'][0]
ego_math['rate']=ego_session['w_math'][0]
ego_verbal['rate']=ego_session['w_verbal'][0]
ego_pop['rate']=ego_session['w_pop'][0]
ego_sports['rate']=ego_session['w_sports'][0]
ego_us['rate']=ego_session['w_us'][0]

# from ego_science remove the prefix 'science_' from the column names that have it
ego_science.columns = [col.replace('science_','') for col in ego_science.columns]

# from ego_math remove the prefix 'math_' from the column names that have it
ego_math.columns = [col.replace('math_','') for col in ego_math.columns]

# from ego_verbal remove the prefix 'verbal_' from the column names that have it
ego_verbal.columns = [col.replace('verbal_','') for col in ego_verbal.columns]

# from ego_pop remove the prefix 'pop_' from the column names that have it
ego_pop.columns = [col.replace('pop_','') for col in ego_pop.columns]

# from ego_sports remove the prefix 'sports_' from the column names that have it
ego_sports.columns = [col.replace('sports_','') for col in ego_sports.columns]

# from ego_us remove the prefix 'us_' from the column names that have it
ego_us.columns = [col.replace('us_','') for col in ego_us.columns]

# stack all the topic tables into one larger data frame called ego_updates
ego_updates = pd.concat([ego_science, ego_math, ego_verbal, ego_pop, ego_sports, ego_us])
ego_updates.reset_index(inplace=True, drop=True)

# add a colun that indicates the treatment
ego_updates['treatment'] = 'ego'

# turn the type column into an integer
ego_updates['type'] = ego_updates['type'].astype(int)

# add a column that indicates if the participant was overconfident
ego_updates['overconfident'] = 0
ego_updates.loc[ego_updates['type']<ego_updates['belief'], 'overconfident'] = 1

# add a column that indicates if the participant was underconfident
ego_updates['underconfident'] = 0
ego_updates.loc[ego_updates['type']>ego_updates['belief'], 'underconfident'] = 1

# add a column that indicates if the participant was correct
ego_updates['correct']=0
ego_updates.loc[ego_updates['type']==ego_updates['belief'], 'correct'] = 1

# create a table for each pair of theta and omega (type and rate) the subindexes are in that order
#low types
updates_ll = ego_updates.loc[(ego_updates['type']==0) & (ego_updates['rate']==0), :]
updates_lm = ego_updates.loc[(ego_updates['type']==0) & (ego_updates['rate']==1), :]
updates_lh = ego_updates.loc[(ego_updates['type']==0) & (ego_updates['rate']==2), :]

# mid types
updates_ml = ego_updates.loc[(ego_updates['type']==1) & (ego_updates['rate']==0), :]
updates_mm = ego_updates.loc[(ego_updates['type']==1) & (ego_updates['rate']==1), :]
updates_mh = ego_updates.loc[(ego_updates['type']==1) & (ego_updates['rate']==2), :]

# high types
updates_hl = ego_updates.loc[(ego_updates['type']==2) & (ego_updates['rate']==0), :]
updates_hm = ego_updates.loc[(ego_updates['type']==2) & (ego_updates['rate']==1), :]
updates_hh = ego_updates.loc[(ego_updates['type']==2) & (ego_updates['rate']==2), :]

# add the type of misspecification
ego_updates.loc[ego_updates['overconfident']==1, 'misspecification'] = 'over'
ego_updates.loc[ego_updates['underconfident']==1, 'misspecification'] = 'under'
ego_updates.loc[ego_updates['correct']==1, 'misspecification'] = 'correct'

ego_updates.to_csv('Clean/ego_updates.csv', index=False)

################# the stereotype treatment #################

# from the data frame select all the columns that have names that start with 'Quizzes' and append the column 'participant.code
quiz_cols = [col for col in stereo_wide.columns if 'Quizzes' in col]+['participant.code', 'treatment']


# from the data frame select all the columns that have names that start with 'participant.'
participant_cols = [col for col in stereo_wide.columns if 'participant' in col]+['participant.code']

# from the data frame select all the columns that have names that start with 'session.'
session_cols = [col for col in stereo_wide.columns if 'session' in col]+['participant.code']

# from the data frame select all the columns that have names that start with 'Signals.'
signal_cols = [col for col in stereo_wide.columns if 'Signals' in col]+['participant.code']

# from the data frame select all the columns that have names that start with 'SignalsOther.'
signal_other_cols = [col for col in stereo_wide.columns if 'SignalsOther' in col]+['participant.code']

# from the data frame select all the columns that have names that start with 'Questionnaire.'
questionnaire_cols = [col for col in stereo_wide.columns if 'Questionnaire' in col]+['participant.code']

# split the data frame stereo_wide into 6 data frames using the columns we just selected
stereo_quiz = stereo_wide[quiz_cols]
stereo_participant = stereo_wide[participant_cols]
stereo_session = stereo_wide[session_cols]
stereo_signal = stereo_wide[signal_cols] # this has no information for the stereotype treatment
stereo_signal_other = stereo_wide[signal_other_cols] 
stereo_questionnaire = stereo_wide[questionnaire_cols]

# for stereo_quiz rename all the columns to remove the prefix 'Quizzes'
stereo_quiz.columns = [col.replace('Quizzes.','') for col in stereo_quiz.columns]
# for stereo_quiz rename all the columns to remove the prefix 'player'
stereo_quiz.columns = [col.replace('player.','') for col in stereo_quiz.columns]

# drop all the columns that have either 'group.' or 'subsession.' in the name
stereo_quiz = stereo_quiz[[col for col in stereo_quiz.columns if 'group.' not in col and 'subsession.' not in col]]
# melt the data making the participant code the id variable
stereo_quiz_long = pd.melt(stereo_quiz, id_vars=['participant.code'])
# split the variable column into two columns, one for the round_number and one for the question
stereo_quiz_long[['round_number','variable_name']] = stereo_quiz_long['variable'].str.split('.', expand=True)
# drop the column variable with the long names
stereo_quiz_long = stereo_quiz_long.drop('variable', axis=1)
# reshape stereo_quiz_long from long to wide format by making each of the values in variable_name a column
stereo_quiz_wide = stereo_quiz_long.pivot(index=['participant.code','round_number'], columns=['variable_name'], values='value')
# make a table that has only the score for each topic and the participant code
stereo_scores = stereo_quiz_wide[['topic', 'score']]
# reset the index so that participant_code is just another colum
stereo_scores.reset_index(inplace=True)

# Rename all the other variables withoutht the 'participant.' prefix
stereo_participant.columns = [col.replace('participant.','') for col in stereo_participant.columns]

### Main part of the experiment for the sterotype treatment

# remove the 'Signals.' prefix from all the column names and the 'participant.' prefix from the code column
stereo_signal_other.columns = [col.replace('SignalsOther.','') for col in stereo_signal_other.columns]
stereo_signal_other.columns = [col.replace('participant.','') for col in stereo_signal_other.columns]
# replace the 'player.' in the names of the columns
stereo_signal_other.columns = [col.replace('player.', '') for col in stereo_signal_other.columns]

# drop the group and subsession level columns
stereo_signal_other = stereo_signal_other[[col for col in stereo_signal_other.columns if 'group.' not in col and '.subsession' not in col]]

# melt the data set making code the id column. then split all the variable names
stereo_signal_other_long = pd.melt(stereo_signal_other, id_vars='code')

# split the variable column into two columns, one for the round_number and one for the question
stereo_signal_other_long[['round_number','variable_name']] = stereo_signal_other_long['variable'].str.split('.', expand=True)
# drop the column variable with the long names
stereo_signal_other_long = stereo_signal_other_long.drop('variable', axis=1)

# reshape stereo_signal_other_long from long to wide format by making each of the values in variable_name a column
stereo_signal_other_wide = stereo_signal_other_long.pivot(index=['code','round_number'], columns=['variable_name'], values='value')
stereo_signal_other_wide.reset_index(inplace=True)

beliefs_other = stereo_signal_other_wide.loc[stereo_signal_other_wide['science_belief_other']>=0, 
                    ['code','science_belief_other', 'us_belief_other', 'math_belief_other', 'verbal_belief_other', 
                    'pop_belief_other', 'sports_belief_other',
                    'science_certainty_other', 'us_certainty_other', 'math_certainty_other', 'verbal_certainty_other', 
                    'pop_certainty_other', 'sports_certainty_other']]

# the round_numbers range from 1 to 60. I want all of them to range from 1 to 10 by setting 11 to 1, 21 to 1, 12 to 2, etc.
stereo_signal_other_wide['round_number'] = stereo_signal_other_wide['round_number'].astype(int)

stereo_signal_other_wide['round_number'].replace([12,23,34,45,56], 1, inplace=True)
stereo_signal_other_wide['round_number'].replace([13,24,35,46,57], 2, inplace=True)
stereo_signal_other_wide['round_number'].replace([14,25,36,47,58], 3, inplace=True)
stereo_signal_other_wide['round_number'].replace([15,26,37,48,59], 4, inplace=True)
stereo_signal_other_wide['round_number'].replace([16,27,38,49,60], 5, inplace=True)
stereo_signal_other_wide['round_number'].replace([17,28,39,50,61], 6, inplace=True)
stereo_signal_other_wide['round_number'].replace([18,29,40,51,62], 7, inplace=True)
stereo_signal_other_wide['round_number'].replace([19,30,41,52,63], 8, inplace=True)
stereo_signal_other_wide['round_number'].replace([20,31,42,53,64], 9, inplace=True)
stereo_signal_other_wide['round_number'].replace([21,32,43,54,65], 10, inplace=True)
stereo_signal_other_wide['round_number'].replace([22,33,44,55,66], 11, inplace=True)

# split by topic

st_science = stereo_signal_other_wide.loc[(stereo_signal_other_wide['effort']>=0) & (stereo_signal_other_wide['topic']=='Science and Technology'), 
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'science_other', 'topic', 'signal']]
# impute the values for science_belief and the science_certainty from the table beliefs
st_science = st_science.merge(beliefs_other[['code', 'science_belief_other', 'science_certainty_other']], on='code', how='left')

# add a column with the type according to the science score
st_science.loc[st_science['science_other']>15, 'type'] = '2'
st_science.loc[st_science['science_other']<=15, 'type'] = '1'
st_science.loc[st_science['science_other']<6, 'type'] = '0'

# make a data frame for math exactly as st_science but with the math score and belief
st_math = stereo_signal_other_wide.loc[(stereo_signal_other_wide['effort']>=0) & (stereo_signal_other_wide['topic']=='Math'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'math_other', 'topic', 'signal']]
# impute the values for math_belief and the math_certainty from the table beliefs
st_math = st_math.merge(beliefs_other[['code', 'math_belief_other', 'math_certainty_other']], on='code', how='left')

# add a column with the type according to the science score
st_math.loc[st_math['math_other']>15, 'type'] = '2'
st_math.loc[st_math['math_other']<=15, 'type'] = '1'
st_math.loc[st_math['math_other']<6, 'type'] = '0'

# make a data frame for verbal exactly as st_science but with the verbal score and belief
st_verbal = stereo_signal_other_wide.loc[(stereo_signal_other_wide['effort']>=0) & (stereo_signal_other_wide['topic']=='Verbal'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'verbal_other', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
st_verbal = st_verbal.merge(beliefs_other[['code', 'verbal_belief_other', 'verbal_certainty_other']], on='code', how='left')

# add a column with the type according to the science score
st_verbal.loc[st_verbal['verbal_other']>15, 'type'] = '2'
st_verbal.loc[st_verbal['verbal_other']<=15, 'type'] = '1'
st_verbal.loc[st_verbal['verbal_other']<6, 'type'] = '0'

# make a data frame for verbal exactly as st_science but with the verbal score and belief
st_pop = stereo_signal_other_wide.loc[(stereo_signal_other_wide['effort']>=0) & (stereo_signal_other_wide['topic']=='Pop-Culture and Art'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'pop_other', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
st_pop = st_pop.merge(beliefs_other[['code', 'pop_belief_other', 'pop_certainty_other']], on='code', how='left')

# add a column with the type according to the science score
st_pop.loc[st_pop['pop_other']>15, 'type'] = '2'
st_pop.loc[st_pop['pop_other']<=15, 'type'] = '1'
st_pop.loc[st_pop['pop_other']<6, 'type'] = '0'

# make a data frame for verbal exactly as st_science but with the verbal score and belief
st_sports = stereo_signal_other_wide.loc[(stereo_signal_other_wide['effort']>=0) & (stereo_signal_other_wide['topic']=='Sports and Video Games'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'sports_other', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
st_sports = st_sports.merge(beliefs_other[['code', 'sports_belief_other', 'sports_certainty_other']], on='code', how='left')

# add a column with the type according to the science score
st_sports.loc[st_sports['sports_other']>15, 'type'] = '2'
st_sports.loc[st_sports['sports_other']<=15, 'type'] = '1'
st_sports.loc[st_sports['sports_other']<6, 'type'] = '0'

# make a data frame for verbal exactly as st_science but with the verbal score and belief
st_us = stereo_signal_other_wide.loc[(stereo_signal_other_wide['effort']>=0) & (stereo_signal_other_wide['topic']=='US Geography'),
                    ['code', 'round_number', 'effort', 'fails', 'last_button', 'us_other', 'topic', 'signal']]
# impute the values for verbal_belief and the verbal_certainty from the table beliefs
st_us = st_us.merge(beliefs_other[['code', 'us_belief_other', 'us_certainty_other']], on='code', how='left')

# add a column with the type according to the science score
st_us.loc[st_us['us_other']>15, 'type'] = '2'
st_us.loc[st_us['us_other']<=15, 'type'] = '1'
st_us.loc[st_us['us_other']<6, 'type'] = '0'

# from the ego session data frame select only the columns that we will use
stereo_session = stereo_session[['participant.id_in_session', 
                            'session.code', 
                            'session.w_verbal', 
                            'session.w_math', 
                            'session.w_pop',
                            'session.w_science',
                            'session.w_sports',
                            'session.w_us']]


# in stero_session remove the prefixes 'participant.' and 'session.' from the column names
stereo_session.columns = [col.replace('participant.','') for col in stereo_session.columns]
stereo_session.columns = [col.replace('session.','') for col in stereo_session.columns]
# add a column to each of the topics tables with the corresponding value of w from the stereo_session table
st_science['rate']=stereo_session['w_science'][0]
st_math['rate']=stereo_session['w_math'][0]
st_verbal['rate']=stereo_session['w_verbal'][0]
st_pop['rate']=stereo_session['w_pop'][0]
st_sports['rate']=stereo_session['w_sports'][0]
st_us['rate']=stereo_session['w_us'][0]

# from st_science rename the score_other column to score so that it we can stack across all the topics and the belief and
# crtainty columns to not include the topic '_prefix' or the other '_suffix'
st_science.rename(columns={'science_other':'score', 'science_belief_other':'belief', 'science_certainty_other':'certainty'}, inplace=True)
st_math.rename(columns={'math_other':'score', 'math_belief_other':'belief', 'math_certainty_other':'certainty'}, inplace=True)
st_verbal.rename(columns={'verbal_other':'score', 'verbal_belief_other':'belief', 'verbal_certainty_other':'certainty'}, inplace=True)
st_pop.rename(columns={'pop_other':'score', 'pop_belief_other':'belief', 'pop_certainty_other':'certainty'}, inplace=True)
st_sports.rename(columns={'sports_other':'score', 'sports_belief_other':'belief', 'sports_certainty_other':'certainty'}, inplace=True)
st_us.rename(columns={'us_other':'score', 'us_belief_other':'belief', 'us_certainty_other':'certainty'}, inplace=True)


# stack all the topic tables into one larger data frame called st_updates
st_updates = pd.concat([st_science, st_math, st_verbal, st_pop, st_sports, st_us])
st_updates.reset_index(inplace=True, drop=True)

# add a colun that indicates the treatment
st_updates['treatment'] = 'stereotype'

# turn the type column into an integer
st_updates['type'] = st_updates['type'].astype(int)

# add a column that indicates if the participant was overconfident
st_updates['overconfident'] = 0
st_updates.loc[st_updates['type']<st_updates['belief'], 'overconfident'] = 1

# add a column that indicates if the participant was underconfident
st_updates['underconfident'] = 0
st_updates.loc[st_updates['type']>st_updates['belief'], 'underconfident'] = 1

# add a column that indicates if the participant was correct
st_updates['correct']=0
st_updates.loc[st_updates['type']==st_updates['belief'], 'correct'] = 1

# create a table for each pair of theta and omega (type and rate) the subindexes are in that order
#low types
updates_ll = st_updates.loc[(st_updates['type']==0) & (st_updates['rate']==0), :]
updates_lm = st_updates.loc[(st_updates['type']==0) & (st_updates['rate']==1), :]
updates_lh = st_updates.loc[(st_updates['type']==0) & (st_updates['rate']==2), :]

# mid types
updates_ml = st_updates.loc[(st_updates['type']==1) & (st_updates['rate']==0), :]
updates_mm = st_updates.loc[(st_updates['type']==1) & (st_updates['rate']==1), :]
updates_mh = st_updates.loc[(st_updates['type']==1) & (st_updates['rate']==2), :]

# high types
updates_hl = st_updates.loc[(st_updates['type']==2) & (st_updates['rate']==0), :]
updates_hm = st_updates.loc[(st_updates['type']==2) & (st_updates['rate']==1), :]
updates_hh = st_updates.loc[(st_updates['type']==2) & (st_updates['rate']==2), :]

st_updates.loc[st_updates['overconfident']==1, 'misspecification'] = 'over'
st_updates.loc[st_updates['underconfident']==1, 'misspecification'] = 'under'
st_updates.loc[st_updates['correct']==1, 'misspecification'] = 'correct'

################# MERGE TREARMENTS ####################
# merge the data from both treatments into a table called updates
updates = pd.concat([ego_updates, st_updates])

# add a column that turns the misspecification column into a numeric variable. -1 if under, 0 if correct and 1 if over
updates['misspecification_num'] = 0
updates.loc[updates['misspecification']=='over', 'misspecification_num'] = 1
updates.loc[updates['misspecification']=='under', 'misspecification_num'] = -1

# assign a number code to each of the topics to create an id column that has the participant code and the topic they were updating on.
updates.loc[updates['topic']=='Math', 'topic_num'] = '1'
updates.loc[updates['topic']=='Science and Technology', 'topic_num'] = '2'
updates.loc[updates['topic']=='Verbal', 'topic_num'] = '3'
updates.loc[updates['topic']=='Pop-Culture and Art', 'topic_num'] = '4'
updates.loc[updates['topic']=='Sports and Video Games', 'topic_num'] = '5'
updates.loc[updates['topic']=='US Geography', 'topic_num'] = '6'

# make a column that combines the participant code and the topic number into a singe id for a participant in a task.
updates['player_code'] = updates['code']+updates['topic_num']

updates.reset_index(inplace=True)
 
# need to rename the columns type and rate from updates to theta and omega
updates = updates.rename(columns={'type':'theta', 'rate':'omega'})

### Add columns to determine how the Subject's beliefs about their type changed across rounds
# for each task, determine whether their belief changed from the initial belief or not.
# check at every row if the belief is different from the last_button. 
updates['current_belief_start'] = updates['last_button'] - updates['belief']

# for rows in which rond_number is 2 or more, check if last_button is the same as last_button in the previous round_number for that player_code
# and register the size of the belief change in the column belief_change
updates['belief_change'] = np.where(updates['round_number']>1, 
                                     updates['last_button'] - updates['last_button'].shift(1), 
                                     updates['current_belief_start'])

# create a column that indicates if the belief changed or not in that round relative to the previous round
updates['change_indicator'] = 0
updates.loc[updates['belief_change']!=0, 'change_indicator'] = 1
# split the sample into two. Those who never changed their belief and those who did
# to do so, first group by player_code and then check if the sum of the change_indicator is 0 or not
updates['change_indicator_sum'] = updates.groupby('player_code')['change_indicator'].transform('sum')

## Likelihoods
#for each subject, calulate the likelihood of each of the types given the signals they saw.
# the probability matrices are needed for th calculatin of the likelihood
ml = np.array([[.20, .25, .40], [.07, .30, .45], [.02, .20, .50]])
mm = np.array([[.40, .45, .65], [.30, .65, .69], [.05, .50, .80]])
mh = np.array([[.45, .55, .75], [.35, .69, .80], [.25, .65, .98]])

msc = [ml, mm, mh]

for i in range(len(updates['player_code'].unique())):
    # get a single path for a single player
    c = updates['player_code'].unique()[i]
    player = updates.loc[updates['player_code']==c, :]
    # for each round get the history of (effort, signal) pairs up to that round
    p_t=[]
    lr_t=[]
    prior = [1/3, 1/3, 1/3]

    for t in range(11):
        
        e_t = int(player.loc[player['round_number']==t+1, 'effort'])
        theta = int(player.loc[player['round_number']==t+1, 'theta'])
        belief = int(player.loc[player['round_number']==t+1, 'belief'])
        omega = int(player.loc[player['round_number']==t+1, 'omega'])
        s_t = int(player.loc[player['round_number']==t+1, 'signal'])
        f_t = 10-s_t

        # update the belief about omega for each of the types separately
        posterior_true = np.diag(np.diagflat(prior)@np.diagflat(sp.stats.binom.pmf(s_t, 10, msc[theta][e_t, :], loc=0)))/sum(np.diag(np.diagflat(prior)@np.diagflat(sp.stats.binom.pmf(s_t, 10, msc[theta][e_t, :], loc=0))))
        posterior_belief = np.diag(np.diagflat(prior)@np.diagflat(sp.stats.binom.pmf(s_t, 10, msc[belief][e_t, :], loc=0)))/sum(np.diag(np.diagflat(prior)@np.diagflat(sp.stats.binom.pmf(s_t, 10, msc[belief][e_t, :], loc=0))))

        p_true = sp.stats.binom.pmf(s_t, 10, msc[theta][e_t, :], loc=0)@posterior_true
        p_belief = sp.stats.binom.pmf(s_t, 10, msc[belief][e_t, :], loc=0)@posterior_belief
        # multiply all the elements in p_true and p_belief
        l_true = np.prod(p_true)
        l_belief = np.prod(p_belief)
        # calculate the likelihood ratio
        lr_t.append(l_true/l_belief)
    # add a column to the updates data frame with the likelihood ratio for each round
    updates.loc[updates['player_code']==c, 'lr'] = lr_t

# save the table updates as a csv file
updates.to_csv('Clean/updates.csv', index=False)

ego_updates.to_csv('Clean/ego_updates.csv', index=False)




