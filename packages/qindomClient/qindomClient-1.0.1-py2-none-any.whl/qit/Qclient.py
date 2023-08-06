import json

import requests

from qit.config import *


class Qclient:

    def __init__(self, username):
        self.username = username

    def _train(self, training_data, label, clf_type, s3=False, auto_adjust=True, n_estimators=None, random_state=None,
               max_depth=None, lmd=None, kernel=None, n_neighbors=None, verbose=None, gamma=None, c=None):
        request_dict = dict()

        if n_estimators is not None:
            if not isinstance(n_estimators, int):
                raise TypeError('n_estimators expects integer')
            else:
                request_dict[N_ESTIMATORS] = n_estimators

        if random_state is not None:
            if not isinstance(random_state, int):
                raise TypeError('random_estimators expects integer')
            else:
                request_dict[RANDOM_STATE] = random_state

        if max_depth is not None:
            if not isinstance(max_depth, int):
                raise TypeError('max_depth expects integer')
            else:
                request_dict[MAX_DEPTH] = max_depth

        if lmd is not None:
            if not isinstance(lmd, (float, int)):
                raise TypeError('lmd expects float')
            else:
                request_dict[LMD] = lmd

        if kernel is not None:
            if not isinstance(kernel, str):
                raise TypeError('kernel expects str')
            else:
                request_dict[KERNEL] = kernel

        if n_neighbors is not None:
            if not isinstance(n_neighbors, int):
                raise TypeError('n_neighbors expects integer')
            else:
                request_dict[N_NEIGHBORS] = n_neighbors

        if verbose is not None:
            if not isinstance(verbose, int):
                raise TypeError('verbose expects integer')
            else:
                request_dict[VERBOSE] = verbose

        if gamma is not None:
            if not isinstance(gamma, str):
                raise TypeError('gamma expects String')
            else:
                request_dict[GAMMA] = gamma

        if c is not None:
            if not isinstance(c, (float, int)):
                raise TypeError('c expects float')
            else:
                request_dict[C] = c

        if clf_type not in CLF_LIST:
            raise TypeError(clf_type, " is not in classifier list, expected classifiers are: ", CLF_LIST)
        else:
            request_dict[CLF] = clf_type

        data_object = dict()
        if s3:
            request_dict[DATA] = training_data
        else:
            if not isinstance(training_data, list):
                raise TypeError('train_data expects a list of list floats')
            if not all(isinstance(x, list) for x in training_data):
                raise TypeError('train_data expects a list of list floats')
            for first_list in training_data:
                for x in first_list:
                    if not isinstance(x, (float, int)):
                        raise TypeError('training_data expects list of list floats')
            data_object[TRAINING_DATA] = training_data

            if not isinstance(label, list):
                raise TypeError('label expects a list')
            if not all(isinstance(x, (float, int)) for x in label):
                raise TypeError('train_data expects a list with all floats')
            data_object[LABEL] = label

            request_dict[DATA] = json.dumps(data_object)

        request_dict[S3] = s3
        request_dict[AUTO_ADJ] = auto_adjust

        headers = {'content-type': 'application/json'}

        r = requests.post('%s/%s/%s' % (SERVICE_URL, 'model/train', self.username), json=request_dict, headers=headers)
        r.raise_for_status()
        return r.json()

    def getMethods(self):
        return CLF_LIST

    def train_model_sync(self, training_data, label, clf_type, auto_adjust=True, n_estimators=None, random_state=None,
                         max_depth=None, lmd=None, kernel=None, n_neighbors=None, verbose=None, gamma=None, c=None):
        return self._train(training_data, label, clf_type, auto_adjust=auto_adjust, n_estimators=n_estimators,
                           random_state=random_state,
                           max_depth=max_depth, lmd=lmd, kernel=kernel, n_neighbors=n_neighbors, verbose=verbose,
                           gamma=gamma, c=c)

    def train_model_s3(self, training_data, clf_type, auto_adjust=True, n_estimators=None, random_state=None,
                       max_depth=None, lmd=None, kernel=None, n_neighbors=None, verbose=None, gamma=None, c=None):
        return self._train(training_data, None, clf_type, s3=True, auto_adjust=auto_adjust, n_estimators=n_estimators,
                           random_state=random_state,
                           max_depth=max_depth, lmd=lmd, kernel=kernel, n_neighbors=n_neighbors, verbose=verbose,
                           gamma=gamma, c=c)

    def predict_sync(self, test_data, modelId):
        request_dict = dict()
        data_object = dict()
        if not isinstance(test_data, list):
            raise TypeError('test_data expects a list of list floats')
        if not all(isinstance(x, list) for x in test_data):
            raise TypeError('test_data expects a list of list floats')
        for first_list in test_data:
            for x in first_list:
                if not isinstance(x, (float, int)):
                    raise TypeError('test_data expects list of list floats')
        data_object[TEST_DATA] = test_data
        request_dict[DATA] = json.dumps(data_object)
        headers = {'content-type': 'application/json'}
        r = requests.post('%s/%s/%s/%s' % (SERVICE_URL, 'model/predict', self.username, modelId), json=request_dict,
                          headers=headers)
        r.raise_for_status()
        return r.text
