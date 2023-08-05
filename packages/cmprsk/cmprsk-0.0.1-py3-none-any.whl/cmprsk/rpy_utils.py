import enum

import numpy as np
import pandas as pd
import rpy2 as R

from pandas.api.types import is_numeric_dtype
from rpy2 import rinterface
from rpy2 import robjects
from rpy2.robjects.packages import importr

# pandas R interface
from rpy2.robjects import r, pandas2ri, numpy2ri
pandas2ri.activate()
# numpy2ri.activate()

cmprsk = importr('cmprsk')


class Crr_Result(object):
    def __init__(self, r_crr_res):
        self.raw = r_crr_res
        # TODO: finish parsing


class NotImplementedError(Exception):
    pass


class InputError(Exception):
    pass


class Dtypes(enum.Enum):
    int = R.rinterface.INTSXP
    real = R.rinterface.REALSXP
    bool = R.rinterface.LGLSXP


def r_int_vec(np_vec, dtype):
    return R.rinterface.SexpVector(np_vec, dtype.value)


def r_int_vec(np_vec):
    return R.rinterface.SexpVector(np_vec, R.rinterface.INTSXP)


def r_float_vec(np_vec):
    return R.rinterface.SexpVector(np_vec, R.rinterface.REALSXP)


def r_bool_vec(np_vec):
    return R.rinterface.SexpVector(np_vec, R.rinterface.LGLSXP)


def r_vector(np_vector):
    """Convert a numpy vector to an R vector

    Args:
        np_vector (np.array): 1 dimentional array of bool, int or floats

    Returns:
        rpy2.rinterface.SexpVector: R vector of compatible data type
    """

    if np_vector.ndim != 1:
        msg = 'Input niput dimension is %s and MUST be 1' % np_vector.ndim
        raise ValueError(msg)

    d_type = np_vector.dtype
    if np.issubdtype(d_type, np.integer):
        return r_int_vec(np_vector)
    elif np.issubdtype(d_type, np.float):
        return r_float_vec(np_vector)
    elif np.issubdtype(d_type, np.bool):
        return r_bool_vec(np_vector)
    else:
        msg = "Can't convert vectors with dtype %s yet" % d_type
        raise NotImplementedError(msg)


def r_matrix(np_matrix, col_names=None):

    if np_matrix.ndim != 2:
        msg = 'Input input dimension is %s and MUST be 2' % np_matrix.ndim
        raise ValueError(msg)

    n_row, n_col = np_matrix.shape
    r_mat = robject.r.matrix(cov, nrow=n_row, ncol=n_col)
    if col_names is None:
        col_names = ['x_%s' %(i+1) for i in range(n_col)]

    r_mat.colnames = col_names
    return r_mat


def non_numeric_columns(df):
    return [c for c in df.columns if not is_numeric_dtype(df[c])]


def r_dataframe(pd_dataframe):
    return pandas2ri.py2ri(df)


def to_categorical(df, columns):
    """ Creates a COPY and replace the text columns integer values (categories)"""
    _df = df.copy()
    for c in columns:
        _df.loc[:, c] = df[c].astype('category').cat.codes
    return _df


def R_crr(ftime, fstatus, covariates_1):
    """
    Args:
        ftime (np.array):
        fstatus (np.array):
        covariates_1 (pd.DataFrame): numeric only dataframe
        covariates_2 (pd.DataFrame): numeric only dataframe
    """
    non_numeric_cols = non_numeric_columns(covariates_1)
    if non_numeric_cols:
        msg = """

        Input dataframe contains non numeric columns: {}.
        Please convert text columns using `rpy_utils.to_categorical` method first""".format(non_numeric_cols)
        raise InputError(msg)

    r_cov_1 = pandas2ri.py2ri(covariates_1)
    r_ftime = r_vector(ftime)
    r_fstatus = r_vector(fstatus)
    r_crr_result = cmprsk.crr(r_ftime, r_fstatus, r_cov_1)
    return Crr_Result(r_crr_result)


import string
import random

np.random.seed(42)
ftime = np.random.exponential(size=200)
fstatus = np.random.randint(0, 3, 200)
x1 = np.random.exponential(size=200)
x2 = np.random.randn(200)
x0 = [random.choice(string.ascii_lowercase) for _ in range(200)]

cov = pd.DataFrame(dict(x0=x0, x1=x1, x2=x2))

try:
    cov_2 = to_categorical(cov, ['x0'])
    res = R_crr(ftime, fstatus, cov_2)
    print(res.raw)
except Exception as exc:
    print(exc)

try:
    res = R_crr(ftime, fstatus, cov)
except InputError as exc:
    print("caught the right exception")
    print(exc)
