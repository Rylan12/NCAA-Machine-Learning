"""
Make a model to predict upsets
"""
import json
import os
import sys
import warnings
import numpy as np
import pickle
import pandas as pd
from sklearn import linear_model as lm
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import scale, OneHotEncoder

pd.set_option('display.width', 100)
pd.set_option('display.max_columns', 10)

threshold = 0.5

current_tournament_year = 2020

_directory = '/Users/rylanpolster/PycharmProjects/NCAA-Machine-Learning/'

# Ignore warnings
if not sys.warnoptions:
    warnings.simplefilter('default')
    warnings.simplefilter('ignore', category=FutureWarning)
    warnings.simplefilter('ignore', category=DeprecationWarning)
    warnings.simplefilter('ignore', category=PendingDeprecationWarning)


def get_columns():
    # Open columns
    with open(_directory + 'columns.json', 'r') as column_file:
        columns = json.load(column_file)

    columns.remove('TopScore')
    columns.remove('BotScore')
    columns.remove('TopTOV')
    columns.remove('BotTOV')
    columns.remove('TopTOPer')
    columns.remove('BotTOPer')
    columns.remove('TopTSPer')
    columns.remove('BotTSPer')
    columns.remove('TopFT')
    columns.remove('BotFT')
    columns.remove('TopFTA')
    columns.remove('BotFTA')
    columns.remove('TopFTR')
    columns.remove('BotFTR')
    columns.remove('TopTravel')
    columns.remove('BotTravel')
    columns.remove('TopOppPTS')
    columns.remove('BotOppPTS')

    return columns


def upset(probability, upset_cutoff=threshold):
    return round(probability + 0.5 - upset_cutoff)


def format_data_frame(data, col_labels):
    # don't scale SeedType
    if 'SeedType' in col_labels:
        col_labels.remove('SeedType')
        if len(col_labels) != 0:
            # Convert data to floats
            for column in data:
                if data[column].dtype == 'int64':
                    data[column] = data[column].astype('float64')
            data[col_labels] = scale(data[col_labels])
        col_labels.insert(0, 'SeedType')
    else:
        data[col_labels] = scale(data[col_labels])
    # change SeedTypes to integers in case need to encode later
    data = data.replace(
        ['OneSixteen', 'TwoFifteen', 'ThreeFourteen',
         'FourThirteen', 'FiveTwelve', 'SixEleven',
         'SevenTen', 'EightNine'],
        [1, 2, 3, 4, 5, 6, 7, 8])
    return data


def predict(year: int = current_tournament_year, model: str = 'model', new: bool = True, col_labels: list = None,
            model_type: str = None, matchup: bool = False, current_year: bool = False) -> None:
    """
    Train machine learning model for use

    :param current_year: Whether the selected year is the current year or not
    :param year: Year to run predictions for
    :param model: Model name
    :param new: Whether or not to create and train a new model
    :param col_labels: Columns to include in analysis
    :param model_type: Type of model to use ('forest', 'gbc', 'svm', or None for logistic regression)
    :param matchup: Whether of not to run the model based on a specific matchup
    :returns: None
    """

    # Initialize Data
    data = pd.read_csv(_directory + ('./datafile.csv' if not matchup else './Matchup/matchup.csv'))
    current = pd.read_csv(
        _directory + ('./current.csv' if not matchup else './Matchup/matchup.csv')) if current_year else data
    # data = pd.read_csv('NCAA2001_2017.csv')
    # data_2018 = pd.read_csv('NCAA2018.csv')
    # data_2018['year'] = 2018
    # data = data.append(data_2018, sort=True)
    model_file_path = _directory + 'Models/' + model + '.pickle'
    try:
        with open(model_file_path, 'rb') as _:
            # new is False so algorithm will continue with existing model
            pass
    except FileNotFoundError:
        # new was False but algorithm was not found
        print('Model not found. Creating new model...')
        new = True

    # data to pull from the data frame
    if col_labels is None:
        '''
        col_labels = [
                'TopEFGPer', # effective field goal percentage
                'TopFTR', # free throw rate
                'TopTOPer', # turnover percentage
                'TopDRTG', # defensive rating
                'TopSOS', # strength of schedule
                'BotEFGPer',
                'BotFTR',
                'BotTOPer',
                'BotDRTG',
                'BotSOS'
                ]'''
        col_labels = get_columns()

    data = format_data_frame(data, col_labels)
    current = format_data_frame(current, col_labels)

    # current input set
    if not current_year:
        test = data.loc[data['year'] == year][col_labels]
    else:
        test = current[col_labels]

    # results to display
    results_columns = ['SeedType', 'TopSeed', 'BotSeed', 'Upset']
    # results_columns = ['TopSeed', 'BotSeed', 'Upset']
    test_results = current.loc[current['year'] == year][results_columns]

    # Create or Retrieve Model
    # if creating new model
    if new:
        # collect data from correct year and columns
        # training set inputs
        train = data.loc[(data['year'] != year) &
                         (data['year'] != current_tournament_year)][col_labels]

        # create training set answers
        # training set outputs
        train_results = data.loc[(data['year'] != year) &
                                 (data['year'] != current_tournament_year)]['Upset']  # not a df

        # have to one-hot the seeding type if that's in there
        if 'SeedType' in col_labels:
            enc = OneHotEncoder(categorical_features=[0])  # must be first
            train = enc.fit_transform(train).toarray()
            test = enc.fit_transform(test).toarray()
        else:
            train = train.as_matrix()
            test = test.as_matrix()

        # choose model type
        if model_type == 'forest':
            model = RandomForestClassifier()
        elif model_type == 'gbc':
            model = GradientBoostingClassifier()
        elif model_type == 'svc':
            model = SVC(probability=True)
        else:
            model = lm.LogisticRegression()

        # fit data to model (train)
        model.fit(train, train_results.as_matrix())

        # save model
        if not os.path.exists(_directory + 'Models/'):
            os.makedirs(_directory + 'Models')
        with open(model_file_path, 'wb') as model_file:
            pickle.dump(model, model_file)

    # get model
    else:
        # get model
        with open(model_file_path, 'rb') as model_file:
            model = pickle.load(model_file)

        # have to one-hot the seeding type if that's in there
        if 'SeedType' in col_labels:
            enc = OneHotEncoder(categorical_features=[0])  # must be first
            test = enc.fit_transform(test).toarray()
        else:
            test = test.as_matrix()

    # Create Predictions
    predictions = model.predict_proba(test)

    # add probability to display output
    probability = []
    for i in range(len(predictions)):
        probability.append(predictions[i][1])  # second column is upset percentage
    test_results['UpsetProbability'] = probability
    test_results['Correct'] = test_results['Upset'] == upset(test_results['UpsetProbability'])

    # calculate total number correct
    test_results['Correct'].replace([True, False], [1, 0], inplace=True)
    num_correct = pd.DataFrame(data=test_results[['Correct']].sum()).T
    num_correct = num_correct.reindex(columns=test_results.columns)

    # change formatting + look for readability
    test_results['Correct'].replace([1, 0], ['', '' if current_year else 'x'], inplace=True)
    test_results['Upset'].replace([0.0, 1.0], [0, 1], inplace=True)

    # test_results.rename(index=str, columns={"Upset": "Actual"})

    # sort predictions
    test_results = test_results.sort_values('UpsetProbability', ascending=0)

    # add sum column + extra formatting
    test_results = test_results.append(num_correct, sort=True)
    test_results.replace(np.nan, '', inplace=True)

    if current_year:
        # TODO: Format data frame for current year (remove correct, change upset to predicted upset
        pass

    # output data
    print('\n\nYear: %d\n' % year)
    print(test_results)
    test_results.to_csv(_directory + '2017thing.csv')


if __name__ == '__main__':
    _directory = ''
    predict(2018)
