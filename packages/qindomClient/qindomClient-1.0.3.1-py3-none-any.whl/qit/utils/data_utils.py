"""
data related utils
"""

import pandas as pd

from sklearn.datasets.mldata import fetch_mldata
from sklearn.datasets import load_breast_cancer, load_digits, load_iris

from qit.utils.preprocess import preprocess_titanic, preprocess_wisc, preprocess_mnist, preprocess_census, \
    preprocess_bank, preprocess_covtype, preprocess_mushrooms, preprocess_biomechanical, preprocess_credit_card, \
    preprocess_german_credit, preprocess_glass, preprocess_human_activity, preprocess_indian_liver, preprocess_pima, \
    preprocess_wine, preprocess_digits, preprocess_iris, preprocess_ad, preprocess_robot, preprocess_steel


def get_data_key_list():
    """ return dataset name list """
    # return ['titanic', 'bank', 'census', 'mnist', 'mushrooms', 'wisc', 'covtype']
    return ['ad', 'mnist_0_1', 'mnist_2_3', 'mnist_4_5', 'bank', 'biomechanical', 'census', 'covtype',
            'covtype_0_of_20', 'covtype_1_of_20', 'covtype_2_of_20', 'credit_card', 'diabetes', 'digits',
            'german_credit', 'glass', 'human_activity', 'indian_liver', 'iris', 'mushrooms', 'robot', 'steel',
            'titanic', 'wine', 'wisc']


def get_data_key_list_fast():
    """ return dataset name list """
    # return ['bank', 'census', 'titanic', 'mnist', 'mushrooms', 'wisc']
    return ['ad', 'mnist_0_1', 'mnist_2_3', 'mnist_4_5', 'wine', 'biomechanical', 'indian_liver', 'iris', 'credit_card',
            'diabetes', 'digits', 'german_credit', 'glass','census', 'mushrooms', 'steel', 'robot', 'titanic', 'bank',
            'wisc', 'covtype_0_of_20', 'covtype_1_of_20', 'covtype_2_of_20', ]

def get_data_key_list_exp():
    """ return dataset name list """
    return ['titanic', 'wine', 'biomechanical', 'indian_liver', 'diabetes', 'german_credit', 'glass',
            'census', 'mushrooms', 'bank', 'wisc', 'credit_card']


def get_small_datasets():
    """return small datasets"""
    return ['glass', 'wisc', 'indian_liver', 'biomechanical', 'diabetes', 'titanic', 'german_credit', 'wine', 'digits',
            'steel', 'bank', 'robot']


def get_data(data_name):
    """ get data by name """
    root_url = 'https://s3.us-east-2.amazonaws.com/qitmldatasets/datasets/'

    list = get_data_key_list()

    if data_name not in list:
        print('dataset not found: %s' % data_name)
        return []

    if data_name == 'ad':
        data = pd.read_csv(root_url + "ad/add.csv")
        data = data.drop('Unnamed: 0', axis=1)
        train_valid_X, train_valid_y = preprocess_ad(data)
    elif data_name == 'bank':
        data = pd.read_csv(root_url + "bank/bank.csv", delimiter=";", header='infer')
        train_valid_X, train_valid_y = preprocess_bank(data)
    elif data_name == 'biomechanical':
        data_2c = pd.read_csv(root_url + "biomechanical/column_2C_weka.csv")
        data_3c = pd.read_csv(root_url + "biomechanical/column_3C_weka.csv")
        train_valid_X, train_valid_y = preprocess_biomechanical(data_2c, data_3c)
    elif data_name == 'census':
        data = pd.read_csv(root_url + "census/adult.csv")
        train_valid_X, train_valid_y = preprocess_census(data)
    elif 'covtype' in data_name:
        data = pd.read_csv(root_url + 'covtype/covtype.csv')
        ind = data_name.split('_')
        if len(ind) > 1:
            train_valid_X, train_valid_y = preprocess_covtype(data, int(ind[1]), int(ind[3]))
        else:
            train_valid_X, train_valid_y = preprocess_covtype(data)
    elif data_name == 'credit_card':
        data = pd.read_csv(root_url + 'credit_card/UCI_Credit_Card.csv')
        train_valid_X, train_valid_y = preprocess_credit_card(data)
    elif data_name == 'diabetes':
        data = pd.read_csv(root_url + 'diabetes/diabetes.csv')
        train_valid_X, train_valid_y = preprocess_pima(data)
    elif data_name == 'digits':
        data = load_digits()
        train_valid_X, train_valid_y = preprocess_digits(data)
    elif data_name == 'german_credit':
        data = pd.read_csv(root_url + 'german_credit/german_credit_data.csv')
        train_valid_X, train_valid_y = preprocess_german_credit(data)
    elif data_name == 'glass':
        data = pd.read_csv(root_url + 'glass/glass.csv')
        train_valid_X, train_valid_y = preprocess_glass(data)
    elif data_name == 'human_activity':
        train = pd.read_csv(root_url + 'human_activity/train.csv')
        test = pd.read_csv(root_url + 'human_activity/test.csv')
        train_valid_X, train_valid_y = preprocess_human_activity(train, test)
    elif data_name == 'indian_liver':
        data = pd.read_csv(root_url + 'indian_liver/indian_liver_patient.csv')
        train_valid_X, train_valid_y = preprocess_indian_liver(data)
    elif data_name == 'iris':
        data = load_iris()
        train_valid_X, train_valid_y = preprocess_iris(data)
    elif 'mnist' in data_name:
        try:
            mnist = fetch_mldata('MNIST original')
            ind = data_name.split('_')
            train_valid_X, train_valid_y = preprocess_mnist(mnist, int(ind[1]), int(ind[2]))
        except Exception as ex:
            print('mnist failed to load. use Iris instead:')

            data = load_iris()
            train_valid_X, train_valid_y = preprocess_iris(data)
    elif data_name == 'mushrooms':
        data = pd.read_csv(root_url + 'mushrooms/mushrooms.csv')
        train_valid_X, train_valid_y = preprocess_mushrooms(data)
    elif data_name == 'robot':
        data = pd.read_csv(root_url + "robot/sensor_readings_24.csv", header=None)
        train_valid_X, train_valid_y = preprocess_robot(data)
    elif data_name == 'steel':
        data = pd.read_csv(root_url + "steel/faults.csv")
        train_valid_X, train_valid_y = preprocess_steel(data)
    elif data_name == 'titanic':
        train = pd.read_csv(root_url + "titanic/train.csv")
        test = pd.read_csv(root_url + "titanic/test.csv")  # This dataset does not contain labels
        # Clean the data and a little feature engineering so we can get reasonable results
        train_valid_X, train_valid_y = preprocess_titanic(train, test)
    elif data_name == 'wine':
        data = pd.read_csv(root_url + 'wine/winequality-red.csv')
        train_valid_X, train_valid_y = preprocess_wine(data)
    elif data_name == 'wisc':
        wisc = load_breast_cancer()
        train_valid_X, train_valid_y = preprocess_wisc(wisc)

    return train_valid_X, train_valid_y


def get_data_summarize(sort_by='samples'):
    """all datasets summarize """
    datasets = get_data_key_list()

    ress = []
    for d in datasets:
        X, y = get_data(d)
        ress.append([d, X.shape[0], X.shape[1]])


    df = pd.DataFrame(ress)
    df.columns = ['name', 'samples', 'features']
    df.sort_values(by=sort_by, ascending=False, inplace=True)
    return df
