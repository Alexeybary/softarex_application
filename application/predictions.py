import pickle
import sklearn
import pandas as pd
import os
filename = 'model_v1.pk'
filename_dir="static/"+filename
os.path.abspath(filename_dir)
with open(os.path.abspath(filename_dir), 'rb') as f:
    loaded_model = pickle.load(f)


def check_file(file):
    if (file == None):
        return False
    if (file.filename.endswith('.csv')):
        return True
    return False


def make_prediction(file):
    data = pd.read_csv(file)
    if 'Id' in data.columns:
        data = data.drop('Id', axis=1)
    if 'City' in data.columns:
        data = data.drop('City', axis=1)
    data.fillna(value=0, inplace=True)
    if 'Type' in data.columns:
        data.loc[data['Type'] == 'MB', 'Type'] = 'DT'
    else:
        raise Exception
    p_cols_true = ['P1', 'P2', 'P6', 'P11', 'P19', 'P20', 'P21', 'P28', 'P37']
    for i in p_cols_true:
        if i not in data.columns:
            raise Exception
    cat_cols = [i for i in list(data.columns)][1:3]
    cat_data = data[cat_cols]
    dummy_features = pd.get_dummies(cat_data)
    if 'Open Date' in data.columns:
        data['OpenDays'] = (pd.to_datetime("07/07/2022") - pd.to_datetime(data['Open Date'])).dt.days.astype('int16')
        data['Year'] = pd.to_datetime(data['Open Date']).dt.year
        data['Month'] = pd.to_datetime(data['Open Date']).dt.month
        data = data.drop('Open Date', axis=1)
    else:
        raise Exception
    p_data = data[p_cols_true]
    time_data_test = data[['OpenDays', 'Year', 'Month']]
    data = pd.concat([dummy_features, time_data_test, p_data], axis=1)
    for element in ['City Group_Big Cities', 'City Group_Other', 'Type_FC', 'Type_IL', 'Type_DT']:
        if element not in data.columns:
            data[[element]] = 0
    if data.shape[1] != 17:
       raise Exception
    return loaded_model.predict(data.values)