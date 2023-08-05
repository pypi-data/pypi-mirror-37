"""Leave one out coding"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders.utils import get_obj_cols, convert_input, get_generated_cols
from sklearn.utils.random import check_random_state

__author__ = 'hbghhy'


class LeaveOneOutEncoder(BaseEstimator, TransformerMixin):
    """Leave one out coding for categorical features.

    Parameters
    ----------

    verbose: int
        integer indicating verbosity of output. 0 for none.
    cols: list
        a list of columns to encode, if None, all string columns will be encoded.
    drop_invariant: bool
        boolean for whether or not to drop columns with 0 variance.
    return_df: bool
        boolean for whether to return a pandas DataFrame from transform (otherwise it will be a numpy array).
    impute_missing: bool
        boolean for whether or not to apply the logic for handle_unknown, will be deprecated in the future.
    handle_unknown: str
        options are 'error', 'ignore' and 'impute', defaults to 'impute', which will impute the category -1. Warning: if
        impute is used, an extra column will be added in if the transform matrix has unknown categories.  This can causes
        unexpected changes in dimension in some cases.
    randomized: bool
        adds normal (Gaussian) distribution noise into training data in order to decrease overfitting (testing data are untouched).
    sigma: float
        standard deviation (spread or "width") of the normal distribution.

    Example
    -------
    >>> from category_encoders import *
    >>> import pandas as pd
    >>> from sklearn.datasets import load_boston
    >>> bunch = load_boston()
    >>> y = bunch.target
    >>> X = pd.DataFrame(bunch.data, columns=bunch.feature_names)
    >>> enc = LeaveOneOutEncoder(cols=['CHAS', 'RAD']).fit(X, y)
    >>> numeric_dataset = enc.transform(X)
    >>> print(numeric_dataset.info())
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 506 entries, 0 to 505
    Data columns (total 13 columns):
    CRIM       506 non-null float64
    ZN         506 non-null float64
    INDUS      506 non-null float64
    CHAS       506 non-null float64
    NOX        506 non-null float64
    RM         506 non-null float64
    AGE        506 non-null float64
    DIS        506 non-null float64
    RAD        506 non-null float64
    TAX        506 non-null float64
    PTRATIO    506 non-null float64
    B          506 non-null float64
    LSTAT      506 non-null float64
    dtypes: float64(13)
    memory usage: 51.5 KB
    None

    References
    ----------

    .. [1] Strategies to encode categorical variables with many categories. from
    https://www.kaggle.com/c/caterpillar-tube-pricing/discussion/15748#143154.



    """

    def __init__(self, verbose=0, cols=None, drop_invariant=False, return_df=True, impute_missing=True,
                 handle_unknown='impute', random_state=None, randomized=False, sigma=0.05):
        self.return_df = return_df
        self.drop_invariant = drop_invariant
        self.drop_cols = []
        self.verbose = verbose
        self.use_default_cols = cols is None # if True, even a repeated call of fit() will select string columns from X
        self.cols = cols
        self._dim = None
        self.mapping = None
        self.impute_missing = impute_missing
        self.handle_unknown = handle_unknown
        self._mean = None
        self.random_state = random_state
        self.randomized = randomized
        self.sigma = sigma

    def fit(self, X, y, **kwargs):
        """Fit encoder according to X and y.

        Parameters
        ----------

        X : array-like, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.

        Returns
        -------

        self : encoder
            Returns self.

        """

        # first check the type
        X = convert_input(X)
        if isinstance(y, pd.DataFrame):
            y = y.iloc[:,0]
        else:
            y = pd.Series(y, name='target')
        if X.shape[0] != y.shape[0]:
            raise ValueError("The length of X is " + str(X.shape[0]) + " but length of y is " + str(y.shape[0]) + ".")

        self._dim = X.shape[1]

        # if columns aren't passed, just use every string column
        if self.use_default_cols:
            self.cols = get_obj_cols(X)

        categories = self.fit_leave_one_out(
            X, y,
            cols=self.cols
        )
        self.mapping = categories

        if self.drop_invariant:
            self.drop_cols = []
            X_temp = self.transform(X)
            generated_cols = get_generated_cols(X, X_temp, self.cols)
            self.drop_cols = [x for x in generated_cols if X_temp[x].var() <= 10e-5]

        return self

    def transform(self, X, y=None):
        """Perform the transformation to new categorical data.

        Parameters
        ----------

        X : array-like, shape = [n_samples, n_features]
        y : array-like, shape = [n_samples] when transform by leave one out
            None, when transform without target information (such as transform test set)

            

        Returns
        -------

        p : array, shape = [n_samples, n_numeric + N]
            Transformed values with encoding applied.

        """

        if self._dim is None:
            raise ValueError('Must train encoder before it can be used to transform data.')

        # first check the type
        X = convert_input(X)

        # then make sure that it is the right size
        if X.shape[1] != self._dim:
            raise ValueError('Unexpected input dimension %d, expected %d' % (X.shape[1], self._dim,))

        # if we are encoding the training data, we have to check the target
        if y is not None:
            if isinstance(y, pd.DataFrame):
                y = y.iloc[:, 0]
            else:
                y = pd.Series(y, name='target')
            if X.shape[0] != y.shape[0]:
                raise ValueError("The length of X is " + str(X.shape[0]) + " but length of y is " + str(y.shape[0]) + ".")

        if not self.cols:
            return X
        X = self.transform_leave_one_out(
            X, y,
            mapping=self.mapping,
            impute_missing=self.impute_missing,
            handle_unknown=self.handle_unknown
        )

        if self.drop_invariant:
            for col in self.drop_cols:
                X.drop(col, 1, inplace=True)

        if self.return_df:
            return X
        else:
            return X.values

    def fit_transform(self, X, y=None, **fit_params):
        """
        Encoders that utilize the target must make sure that the training data are transformed with:
             transform(X, y)
        and not with:
            transform(X)
        """
        return self.fit(X, y, **fit_params).transform(X, y)

    def fit_leave_one_out(self, X_in, y, cols=None):
        X = X_in.copy(deep=True)

        if cols is None:
            cols = X.columns.values

        self._mean = y.mean()
        mapping_out = []

        for col in cols:
            tmp = y.groupby(X[col]).agg(['sum', 'count'])
            tmp['mean'] = tmp['sum'] / tmp['count']
            tmp = tmp.to_dict(orient='index')

            mapping_out.append({'col': col, 'mapping': tmp}, )

        return mapping_out

    def transform_leave_one_out(self, X_in, y, mapping=None, impute_missing=True, handle_unknown='impute'):
        """
        Leave one out encoding uses a single column of floats to represent the means of the target variables.
        """

        X = X_in.copy(deep=True)

        random_state_ = check_random_state(self.random_state)
        for switch in mapping:
            column = switch.get('col')
            transformed_column = pd.Series([np.nan] * X.shape[0], name=column)

            for val in switch.get('mapping'):
                if y is None:
                    transformed_column.loc[X[column] == val] = switch.get('mapping')[val]['mean']
                elif switch.get('mapping')[val]['count'] == 1:
                    transformed_column.loc[X[column] == val] = self._mean
                else:
                    transformed_column.loc[X[column] == val] = (
                        (switch.get('mapping')[val]['sum'] - y[(X[column] == val).values]) / (
                            switch.get('mapping')[val]['count'] - 1)
                    )

            if impute_missing:
                if handle_unknown == 'impute':
                    transformed_column.fillna(self._mean, inplace=True)
                elif handle_unknown == 'error':
                    missing = transformed_column.isnull()
                    if any(missing):
                        raise ValueError('Unexpected categories found in column %s' % column)

            if self.randomized and y is not None:
                transformed_column = (transformed_column * random_state_.normal(1., self.sigma, transformed_column.shape[0]))

            X[column] = transformed_column.astype(float)

        return X
