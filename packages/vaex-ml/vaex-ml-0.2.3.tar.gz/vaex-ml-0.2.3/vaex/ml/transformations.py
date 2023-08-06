import functools
import vaex.dataset
from vaex.serialize import register
import numpy as np
from . import generate
from .state import HasState
from traitlets import Dict, Unicode, List, Int, CFloat, CBool, Any


def dot_product(a, b):
    products = ['%s * %s' % (ai, bi) for ai, bi in zip(a, b)]
    return ' + '.join(products)


@register
class StateTransfer(HasState):
    state = Dict()

    def transform(self, dataset):
        copy = dataset.copy()
        self.state = dict(self.state, active_range=[copy._index_start, copy._index_end])
        copy.state_set(self.state)
        return copy


@register
@generate.register
class PCA(HasState):
    '''Transform a set of features using a Principal Component Analysis'''

    features = List(Unicode())
    n_components = Int(default_value=2)
    eigen_vectors = List(List(CFloat)).tag(output=True)
    eigen_values = List(CFloat).tag(output=True)
    prefix = Unicode(default_value="PCA_")
    means = List(CFloat).tag(output=True)

    def fit(self, dataset, column_names=None, progress=False):
        assert self.n_components <= len(self.features), 'cannot have more components than features'
        C = dataset.cov(self.features, progress=progress)
        eigen_values, eigen_vectors = np.linalg.eigh(C)
        indices = np.argsort(eigen_values)[::-1]
        self.means = dataset.mean(self.features, progress=progress).tolist()
        self.eigen_vectors = eigen_vectors[:, indices].tolist()
        self.eigen_values = eigen_values[indices].tolist()

    def transform(self, dataset, n_components=None):
        n_components = n_components or self.n_components
        copy = dataset.copy()
        name_prefix_offset = 0
        eigen_vectors = np.array(self.eigen_vectors)
        while self.prefix + str(name_prefix_offset) in copy.get_column_names(virtual=True, strings=True):
            name_prefix_offset += 1

        expressions = [copy[feature]-mean for feature, mean in zip(self.features, self.means)]
        for i in range(n_components):
            v = eigen_vectors[:, i]
            expr = dot_product(expressions, v)
            name = self.prefix + str(i + name_prefix_offset)
            copy[name] = expr
        return copy


@register
@generate.register
class LabelEncoder(HasState):
    '''Encode labels with integer value between 0 and num_classes-1.'''
    features = List(Unicode())
    prefix = Unicode(default_value="label_encoded_")
    labels = List(List()).tag(output=True)

    def fit(self, dataset):
        labels = []
        for i in self.features:
            labels.append(np.unique(dataset.evaluate(i)).tolist())
        self.labels = labels

    def transform(self, dataset):
        copy = dataset.copy()
        for i, v in enumerate(self.features):
            name = self.prefix + v
            labels = np.unique(dataset.evaluate(v))
            if len(np.intersect1d(labels, self.labels[i])) < len(labels):
                diff = np.setdiff1d(labels, self.labels[i])
                raise ValueError("%s contains previously unseen labels: %s" % (v, str(diff)))
            # copy[name] = np.searchsorted(self.labels[i], v)
            copy.add_virtual_column(name, 'searchsorted({x}, {v})'.format(x=self.labels[i], v=v))
        return copy


@register
@generate.register
class OneHotEncoder(HasState):
    '''Encode categorical labels according ot the One-Hot scheme.'''
    features = List(Unicode())
    uniques = List(List()).tag(output=True)
    one = Any(1)
    zero = Any(0)
    prefix = Unicode(default_value='')

    def fit(self, dataset):
        '''
        Method that fits the labels according to the One-Hot scheme.

        :param dataset: a vaex dataset
        '''

        uniques = []
        for i in self.features:
            expression = vaex.dataset._ensure_strings_from_expressions(i)
            unique = dataset.unique(expression)
            unique = np.sort(unique) # this can/should be optimized with @delay
            uniques.append(unique.tolist())
        self.uniques = uniques

    def transform(self, dataset):
        '''
        Method that applies the the fitted one-hot encodings to a vaex dataset.

        :param dataset: a vaex dataset
        :return copy: a shallow copy of the input vaex dataset that includes the encodings
        '''

        copy = dataset.copy()
        # for each feature, add a virtual column for each unique entry
        for i, feature in enumerate(self.features):
            for j, value in enumerate(self.uniques[i]):
                column_name= self.prefix + feature + '_' + str(value)
                copy.add_virtual_column(column_name, 'where({feature} == {value}, {one}, {zero})'.format(
                                        feature=feature, value=repr(value), one=self.one, zero=self.zero))
        return copy


@register
@generate.register
class StandardScaler(HasState):
    '''Will translate and scale a set of features using its mean and standard deviation'''

    features = List(Unicode())
    mean = List(CFloat).tag(output=True)
    std = List(CFloat).tag(output=True)
    prefix = Unicode(default_value="standard_scaled_")
    with_mean = CBool(default_value=False)
    with_std = CBool(default_value=False)

    def fit(self, dataset):

        mean = dataset.mean(self.features, delay=True)
        std = dataset.std(self.features, delay=True)

        @vaex.delayed
        def assign(mean, std):
            self.mean = mean.tolist()
            self.std = std.tolist()

        assign(mean, std)
        dataset.executor.execute()

    def transform(self, dataset):
        copy = dataset.copy()
        for i in range(len(self.features)):
            name = self.prefix+self.features[i]
            expression = copy[self.features[i]]
            if self.with_mean:
                expression = expression - self.mean[i]
            if self.with_std:
                expression = expression / self.std[i]
            copy[name] = expression
        return copy


@register
@generate.register
class MinMaxScaler(HasState):
    '''Will scale a set of features from [min, max] to [0, 1)'''

    features = List(Unicode())
    prefix = Unicode(default_value="standard_scaled_")
    fmin = List(CFloat).tag(output=True)
    fmax = List(CFloat).tag(output=True)
    feature_range = List(CFloat).tag(output=True)
    prefix = Unicode(default_value="minmax_scaled_")

    def fit(self, dataset):
        assert len(self.feature_range) == 2, 'feature_range must have 2 elements only'
        minmax = dataset.minmax(self.features)
        self.fmin = minmax[:, 0].tolist()
        self.fmax = minmax[:, 1].tolist()

    def transform(self, dataset):
        copy = dataset.copy()

        for i in range(len(self.features)):
            name = self.prefix + self.features[i]
            a = self.feature_range[0]
            b = self.feature_range[1]
            expr = copy[self.features[i]]
            expr = (b-a)*(expr-self.fmin[i])/(self.fmax[i]-self.fmin[i]) + a
            copy[name] = expr
        return copy
