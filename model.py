"""
Make a model to predict upsets
"""
# import numpy as np
import pandas as pd
from sklearn import linear_model as lm
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import scale, OneHotEncoder

pd.options.display.width = 80


def make_model(col_labels=None, year=2017, model_type=None):
    """make and run model"""
    print('Year: %d' % year)
    data = pd.read_csv('NCAA2001_2017.csv')
    data_2018 = pd.read_csv('NCAA2018.csv')
    data_2018['year'] = 2018
    data = data.append(data_2018)

    # data to pull from the data frame
    if col_labels is None:
        col_labels = [
            'TopEFGPer',  # effective field goal percentage
            'TopFTR',  # free throw rate
            'TopTOPer',  # turnover percentage
            'TopDRTG',  # defensive rating
            'TopSOS',  # strength of schedule
            'BotEFGPer',
            'BotFTR',
            'BotTOPer',
            'BotDRTG',
            'BotSOS'
        ]

    # don't scale SeedType
    if 'SeedType' in col_labels:
        col_labels.remove('SeedType')
        if len(col_labels) != 0:
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

    # collect data from correct year and columns
    # training set inputs
    train = data.loc[(data['year'] != year) &
                     (data['year'] != 2018)][col_labels]

    # create training set answers
    # training set outputs
    train_results = data.loc[(data['year'] != year) &
                             (data['year'] != 2018)]['Upset']  # not a df

    # current input set
    test = data.loc[data['year'] == year][col_labels]
    # results to display
    results_columns = ['SeedType', 'TopSeed', 'BotSeed', 'Upset']
    test_results = data.loc[data['year'] == year][results_columns]

    ##########
    # have to one-hot the seeding type if that's in there
    if 'SeedType' in col_labels:
        enc = OneHotEncoder(categorical_features=[0])  # must be first
        train = enc.fit_transform(train).toarray()
        test = enc.fit_transform(test).toarray()
    else:
        train = train.as_matrix()
        test = test.as_matrix()

    # choose model type
    if model_type == "forest":
        model = RandomForestClassifier()
    elif model_type == "gbc":
        model = GradientBoostingClassifier()
    elif model_type == "svc":
        model = SVC(probability=True)
    else:
        model = lm.LogisticRegression()

    # fit data to model (train)
    model.fit(train, train_results.as_matrix())

    # create predictions
    predictions = model.predict_proba(test)

    # add probability to display output
    probability = []
    for i in range(len(predictions)):
        probability.append(predictions[i][1])  # second column is upset percentage
    test_results['UpsetProbability'] = probability

    # Sort and output predictions
    test_results = test_results.sort_values('UpsetProbability', ascending=0)
    print(test_results)


if __name__ == '__main__':
    make_model()
