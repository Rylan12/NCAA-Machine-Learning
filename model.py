"""
Make a model to predict upsets
"""
import numpy as np
import pandas as pd
from sklearn import linear_model as lm
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.ensemble import GradientBoostingClassifier as gbc
from sklearn.svm import SVC as svc
from sklearn.preprocessing import scale, OneHotEncoder

def make_model(col_labels = None, year = 2017, model_type = None):
    """make and run model"""

    data = pd.read_csv('NCAA2001_2017.csv')
    data_2018 = pd.read_csv('NCAA2018.csv')
    data_2018['year'] = 2018
    data = data.append(data_2018)

    # data to pull from the data frame
    if col_labels is None:
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

    train = data.loc[(data['year'] != year) & \
            (data['year'] != 2018)][col_labels]
    train_results = data.loc[(data['year'] != year) & \
            (data['year'] != 2018)]['Upset'] # not a df

    test = data.loc[data['year'] == year][col_labels]
    results_columns = ['SeedType', 'TopSeed', 'BotSeed', 'Upset']
    test_results = data.loc[data['year'] == year][results_columns]

    # have to one-hot the seeding type if that's in there
    if 'SeedType' in col_labels:
        enc = OneHotEncoder(categorical_features = [0]) # must be first
        train = enc.fit_transform(train).toarray()
        test = enc.fit_transform(test).toarray()
    else:
        train = train.as_matrix()
        test = test.as_matrix()

    # making the model
    if model_type == "forest":
        model = rf()
    elif model_type == "gbc":
        model = gbc()
    elif model_type == "svc":
        model = svc(probability = True)
    else:
        model = lm.LogisticRegression()
    model.fit(train, train_results.as_matrix())

    predictions = model.predict_proba(test)
    proba = []
    for i in range(len(predictions)):
        proba.append(predictions[i][1]) # second column is upset percentage

    test_results['UpsetProba'] = proba
    # May need to change sort to sort_values depending on your python version
    test_results = test_results.sort('UpsetProba', ascending = 0) 

    print(test_results)
