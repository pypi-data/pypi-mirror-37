import os
import warnings
import numpy as np

import vaex
import vaex.dataset
from vaex.utils import InnerNamespace

from .pipeline import Pipeline
from .transformations import PCA, StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder


def iris():
    dirname = os.path.dirname(__file__)
    return vaex.open(os.path.join(dirname, 'iris.hdf5'))

def _iris(name, iris_previous, N):
    filename = os.path.join(vaex.utils.get_private_dir('data'), name + '.hdf5')
    if os.path.exists(filename):
        return vaex.open(filename)
    else:
        iris = iris_previous()
        repeat = int(np.ceil(N / len(iris)))
        ds = vaex.dataset.DatasetConcatenated([iris] * repeat)
        ds.export_hdf5(filename)
        return vaex.open(filename)

def iris_1e4():
    '''Returns the iris set repeated so it include ~1e4 rows'''
    return _iris('iris_1e4', iris, int(1e4))

def iris_subsample(N, error_percentage=5, ds=None):
    '''Returns the iris set repeated so it include ~1e4 rows'''
    #return _iris_subsample('iris_1e4', iris, int(1e4))
    ds = ds or iris()
    ds_out = None
    repeats = int(np.ceil(N / len(ds)))
    for feature in ds.get_column_names():
        if feature in ['random_index']:
            continue
        data = ds[feature].values
        min, max = ds.minmax(feature)
        error = (max - min)/100*error_percentage
        data_out = np.repeat(data, repeats)
        if feature not in ['class_']:
            data_out += np.random.random(len(data_out)) * error
        if ds_out is None:
            ds_out = vaex.from_arrays(feature=data_out)
        else:
            ds_out.add_column(feature, data_out)
    return ds_out


def iris_1e5():
    '''Returns the iris set repeated so it include ~1e5 rows'''
    return _iris('iris_1e5', iris_1e4, int(1e5))

def iris_1e6():
    '''Returns the iris set repeated so it include ~1e6 rows'''
    return _iris('iris_1e6', iris_1e5, int(1e6))

def iris_1e7():
    '''Returns the iris set repeated so it include ~1e7 rows'''
    return _iris('iris_1e7', iris_1e6, int(1e7))

def iris_1e8():
    '''Returns the iris set repeated so it include ~1e8 rows'''
    return _iris('iris_1e8', iris_1e7, int(1e8))

def iris_1e9():
    '''Returns the iris set repeated so it include ~1e8 rows'''
    return _iris('iris_1e9', iris_1e8, int(1e9))

def pca(self, n_components=2, features=None, progress=False):
    '''Requires vaex.ml: Create :class:`vaex.ml.transformations.PCA` and fit it'''
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    pca = PCA(n_components=n_components, features=features)
    pca.fit(self, progress=progress)
    return pca


def label_encoder(self, features=None, prefix='label_encoded_'):
    '''Requires vaex.ml: Create :class:`vaex.ml.transformations.LabelEncoder` and fit it.'''
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    label_encoder = LabelEncoder(features=features, prefix=prefix)
    label_encoder.fit(self)
    return label_encoder


def one_hot_encoder(self, features=None, one=1, zero=0, prefix=''):
    '''
    Requires vaex.ml: Create :class:`vaex.ml.transformations.OneHotEncoder` and fit it.

    :param features: list of features to one-hot encode
    :param one: what value to use instead of "1"
    :param zero: what value to use instead of "0"
    :returns one_hot_encoder: vaex.ml.transformations.OneHotEncoder object
    '''
    if features is None:
        raise ValueError('Please give at least one categorical feature.')
    features = vaex.dataset._ensure_strings_from_expressions(features)
    one_hot_encoder = OneHotEncoder(features=features, one=one, zero=zero, prefix=prefix)
    one_hot_encoder.fit(self)
    return one_hot_encoder


def standard_scaler(self, features=None, with_mean=True, with_std=True):
    '''Requires vaex.ml: Create :class:`vaex.ml.transformations.StandardScaler` and fit it'''
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    standard_scaler = StandardScaler(features=features, with_mean=with_mean, with_std=with_std)
    standard_scaler.fit(self)
    return standard_scaler


def minmax_scaler(self, features=None, feature_range=[0, 1]):
    '''Requires vaex.ml: Create :class:`vaex.ml.transformations.MinMaxScaler` and fit it'''
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    minmax_scaler = MinMaxScaler(features=features, feature_range=feature_range)
    minmax_scaler.fit(self)
    return minmax_scaler


def xgboost_model(self, label, num_round, features=None, copy=False, param={}, prediction_name='xgboost_prediction'):
    '''Requires vaex.ml: create a XGBoost model and train/fit it.

    :param label: label to train/fit on
    :param num_round: number of rounds
    :param features: list of features to train on
    :param bool copy: Copy data or use the modified xgboost library for efficient transfer
    :return vaex.ml.xgboost.XGBModel: fitted XGBoost model
    '''
    from .xgboost import XGBModel
    dataset = self
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    xg = XGBModel(prediction_name=prediction_name, num_round=num_round, features=features, param=param)
    xg.fit(dataset, label, copy=copy)
    return xg

def lightgbm_model(self, label, num_round, features=None, copy=False, param={}, classifier=False, prediction_name='lightgbm_prediction'):
    '''Requires vaex.ml: create a lightgbm model and train/fit it.

    :param label: label to train/fit on
    :param num_round: number of rounds
    :param features: list of features to train on
    :param bool copy: Copy data or use the modified xgboost library for efficient transfer
    :param bool classifier: If true, return a the classifier (will use argmax on the probabilities)
    :return vaex.ml.lightgbm.LightGBMModel or vaex.ml.lightgbm.LightGBMClassifier: fitted LightGBM model
    '''
    from .lightgbm import LightGBMModel, LightGBMClassifier
    dataset = self
    features = features or self.get_column_names()
    features = vaex.dataset._ensure_strings_from_expressions(features)
    cls = LightGBMClassifier if classifier else LightGBMModel
    b = cls(prediction_name=prediction_name, num_round=num_round, features=features, param=param)
    b.fit(dataset, label, copy=copy)
    return b


def state_transfer(self):
    from .transformations import StateTransfer
    state = self.state_get()
    state.pop('active_range') # we are not interested in this..
    return StateTransfer(state=state)


def train_test_split(self, test_size=0.2, strings=True, virtual=True, verbose=True):
    """Will split the dataset in train and test part, assuming it is shuffled.
    """
    if verbose:
        warnings.warn('make sure the dataset is shuffled')
    initial = None
    try:
        assert self.filtered is False, 'filtered dataset not supported yet'
        # full_length = len(self)
        self = self.trim()
        initial = self.get_active_range()
        self.set_active_fraction(test_size)
        test = self.trim()
        __, end = self.get_active_range()
        self.set_active_range(end, self.length_original())
        train = self.trim()
    finally:
        if initial is not None:
            self.set_active_range(*initial)
    return train, test


def add_namespace():
    vaex.dataset.Dataset.ml = InnerNamespace({}, vaex.dataset.Dataset, prefix='ml_')
    # try:
    #     from . import generated
    # except ImportError:
    #     print("importing generated code failed")
    vaex.dataset.Dataset.ml._add(train_test_split=train_test_split)

    def to_xgboost_dmatrix(self, label, features=None, selection=None, blocksize=1000 * 1000):
        """

        label: ndarray containing the labels
        """
        from . import xgboost
        return xgboost.VaexDMatrix(self, label, features=features, selection=selection, blocksize=blocksize)

    vaex.dataset.Dataset.ml._add(to_xgboost_dmatrix=to_xgboost_dmatrix, xgboost_model=xgboost_model,
                                 lightgbm_model=lightgbm_model,
                                 state_transfer=state_transfer,
                                 one_hot_encoder=one_hot_encoder,
                                 label_encoder=label_encoder,
                                 pca=pca,
                                 standard_scaler=standard_scaler,
                                 minmax_scaler=minmax_scaler)
    del to_xgboost_dmatrix

    # named_objects.update({ep.name: ep.load()})
