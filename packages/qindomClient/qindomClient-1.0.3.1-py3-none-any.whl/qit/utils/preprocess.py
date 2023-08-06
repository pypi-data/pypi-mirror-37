import pandas as pd
import numpy as np

# Preprocessing helpers
from sklearn import preprocessing
from sklearn.preprocessing import Imputer, Normalizer, scale, LabelEncoder


def preprocess_bank(data):
    data_new = pd.get_dummies(data, columns=['job', 'marital',
                                             'education', 'default',
                                             'housing', 'loan',
                                             'contact', 'month',
                                             'poutcome'])

    # Class column into binary format
    data_new.y.replace(('yes', 'no'), (1, 0), inplace=True)

    train_valid_X = data_new.drop('y', axis=1).values
    train_valid_y = data_new['y'].values

    # train_valid_y = pd.DataFrame(data_new['y']).values
    # train_valid_X = data_new.drop(['y'], axis=1).values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    train_valid_y = 2 * train_valid_y - 1
    # print(train_valid_y)

    print('Datasets: bank, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_census(data):
    print(data.shape)
    print(data.count()[1])

    df = data[data.occupation != '?']
    df.loc[df['native.country'] != 'United-States', 'native.country'] = 'non_usa'

    df_backup = df

    le = LabelEncoder()
    for i in df.columns:
        df[i] = le.fit_transform(df[i])

    train_valid_X = df.drop('income', axis=1).values
    train_valid_y = df['income'].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    train_valid_y = 2 * train_valid_y - 1
    # print(train_valid_y)

    # quit()
    print('Datasets: census, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_mnist(mnist, label0=0, label1=1):
    train_valid_X = mnist.data
    train_valid_y = mnist.target

    ind = (train_valid_y == label0) | (train_valid_y == label1)
    train_valid_X = train_valid_X[ind]
    train_valid_y = train_valid_y[ind]
    # cast label to binary classification
    train_valid_y = np.where(train_valid_y == label0, -1, 1)

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: mnist %s and %s, ' % (str(label0), str(label1)), 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_wisc(wisc):
    idx = np.arange(len(wisc.target))
    np.random.shuffle(idx)

    # train on a random 2/3 and test on the remaining 1/3
    idx_train = idx[:2 * len(idx) // 3]
    idx_test = idx[2 * len(idx) // 3:]

    train_X = wisc.data[idx_train]
    valid_X = wisc.data[idx_test]

    train_y = 2 * wisc.target[idx_train] - 1  # binary -> spin
    valid_y = 2 * wisc.target[idx_test] - 1

    train_valid_X = np.append(train_X, valid_X, axis=0)
    train_valid_y = np.append(train_y, valid_y, axis=0)

    print('Datasets: wisc, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_titanic(train, test):
    full = train.append(test, ignore_index=True)
    # print('Datasets:', 'full:', full.shape, 'train:', train.shape, 'test:', test.shape)

    # Clean data
    sex = pd.Series(np.where(full.Sex == 'male', 1, 0), name='Sex')  # Convert binary categories to 0 and 1
    sex.head()

    embarked = pd.get_dummies(full.Embarked, prefix='Embarked')  # Convert multiple categories to 1 hot encoding
    embarked.head()

    pclass = pd.get_dummies(full.Pclass, prefix='Pclass')

    # Create dataset
    imputed = pd.DataFrame()

    # Fill missing values of Age with the average of Age (mean)
    imputed['Age'] = full.Age.fillna(full.Age.mean())

    # Fill missing values of Fare with the average of Fare (mean)
    imputed['Fare'] = full.Fare.fillna(full.Fare.mean())

    title = pd.DataFrame()
    # we extract the title from each name
    title['Title'] = full['Name'].map(lambda name: name.split(',')[1].split('.')[0].strip())

    # a map of more aggregated titles
    Title_Dictionary = {
        "Capt": "Officer",
        "Col": "Officer",
        "Major": "Officer",
        "Jonkheer": "Royalty",
        "Don": "Royalty",
        "Sir": "Royalty",
        "Dr": "Officer",
        "Rev": "Officer",
        "the Countess": "Royalty",
        "Dona": "Royalty",
        "Mme": "Mrs",
        "Mlle": "Miss",
        "Ms": "Mrs",
        "Mr": "Mr",
        "Mrs": "Mrs",
        "Miss": "Miss",
        "Master": "Master",
        "Lady": "Royalty"

    }

    # we map each title
    title['Title'] = title.Title.map(Title_Dictionary)
    title = pd.get_dummies(title.Title)
    # title = pd.concat( [ title , titles_dummies ] , axis = 1 )

    title.head()
    ####################################################################

    cabin = pd.DataFrame()

    # replacing missing cabins with U (for Uknown)
    cabin['Cabin'] = full.Cabin.fillna('U')

    # mapping each Cabin value with the cabin letter
    cabin['Cabin'] = cabin['Cabin'].map(lambda c: c[0])

    # dummy encoding ...
    cabin = pd.get_dummies(cabin['Cabin'], prefix='Cabin')

    cabin.head()

    ####################################################################

    # a function that extracts each prefix of the ticket, returns 'XXX' if no prefix (i.e the ticket is a digit)
    def cleanTicket(ticket):
        ticket = ticket.replace('.', '')
        ticket = ticket.replace('/', '')
        ticket = ticket.split()
        ticket = map(lambda t: t.strip(), ticket)
        ticket = list(filter(lambda t: not t.isdigit(), ticket))
        if len(ticket) > 0:
            return ticket[0]
        else:
            return 'XXX'

    ticket = pd.DataFrame()

    # Extracting dummy variables from tickets:
    ticket['Ticket'] = full['Ticket'].map(cleanTicket)
    ticket = pd.get_dummies(ticket['Ticket'], prefix='Ticket')

    ticket.shape
    ticket.head()
    ####################################################################

    family = pd.DataFrame()

    # introducing a new feature : the size of families (including the passenger)
    family['FamilySize'] = full['Parch'] + full['SibSp'] + 1

    # introducing other features based on the family size
    family['Family_Single'] = family['FamilySize'].map(lambda s: 1 if s == 1 else 0)
    family['Family_Small'] = family['FamilySize'].map(lambda s: 1 if 2 <= s <= 4 else 0)
    family['Family_Large'] = family['FamilySize'].map(lambda s: 1 if 5 <= s else 0)

    # Assemble data
    full_X = pd.concat([imputed, embarked, cabin, sex], axis=1)
    full_X.head()

    def simplify_ages(df):
        df.Age = df.Age.fillna(-0.5)
        bins = (-1, 0, 5, 12, 18, 25, 35, 60, 120)
        group_names = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
        categories = pd.cut(df.Age, bins, labels=group_names)
        df.Age = categories
        return df

    def simplify_cabins(df):
        df.Cabin = df.Cabin.fillna('N')
        df.Cabin = df.Cabin.apply(lambda x: x[0])
        return df

    def simplify_fares(df):
        df.Fare = df.Fare.fillna(-0.5)
        bins = (-1, 0, 8, 15, 31, 1000)
        group_names = ['Unknown', '1_quartile', '2_quartile', '3_quartile', '4_quartile']
        categories = pd.cut(df.Fare, bins, labels=group_names)
        df.Fare = categories
        return df

    def format_name(df):
        df['Lname'] = df.Name.apply(lambda x: x.split(' ')[0])
        df['NamePrefix'] = df.Name.apply(lambda x: x.split(' ')[1])
        return df

    def drop_features(df):
        return df.drop(['Ticket', 'Name', 'Embarked'], axis=1)

    def transform_features(df):
        df = simplify_ages(df)
        #     df = simplify_cabins(df)
        df = simplify_fares(df)
        #     df = format_name(df)
        #     df = drop_features(df)
        return df

    # def encode_features(df_train, df_test):
    def encode_features(df_combined):
        features = ['Fare', 'Age', 'Sex']
        #     df_combined = pd.concat([df_train[features], df_test[features]])

        for feature in features:
            le = LabelEncoder()
            le = le.fit(df_combined[feature])
            #         df_train[feature] = le.transform(df_train[feature])
            #         df_test[feature] = le.transform(df_test[feature])
            df_combined[feature] = le.transform(df_combined[feature])
            #     return df_train, df_test
        return df_combined

    full_X = transform_features(full_X)
    # full_X.head()

    full_X = encode_features(full_X)

    train_valid_X = full_X[0:891].values
    train_valid_y = train.Survived.values
    train_valid_y[train_valid_y == 0] = -1

    test_X = full_X[891:].values
    test_y = full[891:].Survived.values

    # train_valid_X = np.array(train_valid_X)
    # train_valid_y = np.array(train_valid_y)
    # test_X = np.array(test_X)
    # test_y = np.array(test_y)

    print('Datasets: titanic, ', 'train_valid_X:', train_valid_X.shape, 'train:', train.shape, 'test_X:', test_X.shape)

    # return train_valid_X, train_valid_y, test_X, test_y
    return train_valid_X, train_valid_y


def preprocess_covtype(df, ind_slice=None, total_slice=None):

    def cast_to_binary_classification(x):
        return -1 if x < 2 else 1

    label = 'Cover_Type'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    if ind_slice is not None:
        train_valid_X = train_valid_X[ind_slice::total_slice]
        train_valid_y = train_valid_y[ind_slice::total_slice]

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: covtype %s of %s, ' % (str(ind_slice), str(total_slice)), 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_mushrooms(df):
    # feature engineering
    labelencoder = LabelEncoder()
    for col in df.columns:
        df[col] = labelencoder.fit_transform(df[col])

    # split
    label = 'class'

    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    train_valid_y = 2 * train_valid_y - 1

    print('Datasets: mushroom, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_wine(df):

    def cast_to_binary_classification(x):
        return -1 if x < 6 else 1

    label = 'quality'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: wine, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_indian_liver(df):

    def cast_to_binary_classification(x):
        return -1 if x == 1 else 1

    # fill na
    df["Albumin_and_Globulin_Ratio"] = df.Albumin_and_Globulin_Ratio.fillna(
        df['Albumin_and_Globulin_Ratio'].mean())

    # encode gender
    df = pd.concat([df, pd.get_dummies(df['Gender'], prefix='Gender')], axis=1)
    df.drop(['Gender'], axis=1, inplace=True)

    label = 'Dataset'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: indian liver, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_biomechanical(df1, df2):

    def cast_to_binary_classification(x):
        return -1 if x != 'Normal' else 1

    # make same name
    df1.rename(columns={'pelvic_tilt numeric': 'pelvic_tilt'}, inplace=True)

    df = pd.concat([df1, df2])

    label = 'class'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: biomechanical, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_glass(df):

    def cast_to_binary_classification(x):
        return -1 if x < 3 else 1

    label = 'Type'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: glass, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_german_credit(df):

    def cast_to_binary_classification(x):
        return -1 if x == 'bad' else 1

    # exclude missing value
    df.drop(columns=['Saving accounts', 'Checking account'], axis=1, inplace=True)

    # one hot encode
    df = pd.get_dummies(df, columns=['Sex', 'Housing', 'Purpose'])

    label = 'Risk'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: german credit, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_credit_card(df):

    def cast_to_binary_classification(x):
        return -1 if x == 0 else 1

    label = 'default.payment.next.month'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: credit card, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_pima(df):

    def cast_to_binary_classification(x):
        return -1 if x == 0 else 1

    label = 'Outcome'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: pima, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_human_activity(df1, df2):
    # big dataset

    df = pd.concat([df1, df2])

    def cast_to_binary_classification(x):
        return -1 if 'WALK' not in x else 1

    label = 'Activity'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: human activity, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_digits(df):
    # load X, y from original dataset
    train_valid_X = df['data']
    train_valid_y = df['target']

    # cast y to -1, 1
    train_valid_y = np.where(train_valid_y < 5, -1, 1)

    # Preprocessing data
    imputer = preprocessing.Imputer()
    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: digits, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_iris(df):
    # load X, y from original dataset
    train_valid_X = df['data']
    train_valid_y = df['target']

    # cast y to -1, 1
    train_valid_y = np.where(train_valid_y < 1, -1, 1)

    # Preprocessing data
    imputer = preprocessing.Imputer()
    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: iris, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_ad(df):
    # replace ? with nan
    def replace_question_mark_with_missing(df):
        for i in df:
            df[i] = df[i].replace('[?]', np.NAN, regex=True).astype('float')
            df[i] = df[i].fillna(df[i].mean())
        return df

    df[['0', '1', '2', '3']] = replace_question_mark_with_missing(df.iloc[:, [0, 1, 2, 3]].copy()).values

    # del columns with nan
    df = df.dropna()

    # cast to binary classification
    def cast_to_binary_classification(x):
        return -1 if 'nonad' in x else 1

    label = '1558'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    # Preprocessing data
    imputer = preprocessing.Imputer()
    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: ad, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_steel(df):
    # preprocess dataset
    conditions = [(df['Pastry'] == 1) & (df['Z_Scratch'] == 0) & (df['K_Scatch'] == 0) & (df['Stains'] == 0) & (
                df['Dirtiness'] == 0) & (df['Bumps'] == 0) & (df['Other_Faults'] == 0),
                  (df['Pastry'] == 0) & (df['Z_Scratch'] == 1) & (df['K_Scatch'] == 0) & (df['Stains'] == 0) & (
                              df['Dirtiness'] == 0) & (df['Bumps'] == 0) & (df['Other_Faults'] == 0),
                  (df['Pastry'] == 0) & (df['Z_Scratch'] == 0) & (df['K_Scatch'] == 1) & (df['Stains'] == 0) & (
                              df['Dirtiness'] == 0) & (df['Bumps'] == 0) & (df['Other_Faults'] == 0),
                  (df['Pastry'] == 0) & (df['Z_Scratch'] == 0) & (df['K_Scatch'] == 0) & (df['Stains'] == 1) & (
                              df['Dirtiness'] == 0) & (df['Bumps'] == 0) & (df['Other_Faults'] == 0),
                  (df['Pastry'] == 0) & (df['Z_Scratch'] == 0) & (df['K_Scatch'] == 0) & (df['Stains'] == 0) & (
                              df['Dirtiness'] == 1) & (df['Bumps'] == 0) & (df['Other_Faults'] == 0),
                  (df['Pastry'] == 0) & (df['Z_Scratch'] == 0) & (df['K_Scatch'] == 0) & (df['Stains'] == 0) & (
                              df['Dirtiness'] == 0) & (df['Bumps'] == 1) & (df['Other_Faults'] == 0),
                  (df['Pastry'] == 0) & (df['Z_Scratch'] == 0) & (df['K_Scatch'] == 0) & (df['Stains'] == 0) & (
                              df['Dirtiness'] == 0) & (df['Bumps'] == 0) & (df['Other_Faults'] == 1)]
    choices = ['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
    df['class'] = np.select(conditions, choices)
    # Dropping redundant column
    # Dropping Hot Encoding Classes
    drp_cols = ['TypeOfSteel_A400', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
    df.drop(choices, inplace=True, axis=1)

    # cast to binary classification
    def cast_to_binary_classification(x):
        return -1 if 'Other_Faults' in x else 1

    label = 'class'

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    # Preprocessing data
    imputer = preprocessing.Imputer()
    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: steels, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y


def preprocess_robot(df):
    # todo: consider use diff in features engineering
    # cast to binary classification
    def cast_to_binary_classification(x):
        return -1 if 'Move-Forward' in x else 1

    label = 24

    df[label] = df[label].apply(cast_to_binary_classification)
    train_valid_X = df.drop(label, axis=1).values
    train_valid_y = df[label].values

    # Preprocessing data
    imputer = preprocessing.Imputer()
    scaler = preprocessing.StandardScaler()
    normalizer = preprocessing.Normalizer()
    centerer = preprocessing.KernelCenterer()

    train_valid_X = scaler.fit_transform(train_valid_X)
    train_valid_X = normalizer.fit_transform(train_valid_X)
    train_valid_X = centerer.fit_transform(train_valid_X)

    print('Datasets: robot, ', 'train_valid_X:', train_valid_X.shape)

    return train_valid_X, train_valid_y
