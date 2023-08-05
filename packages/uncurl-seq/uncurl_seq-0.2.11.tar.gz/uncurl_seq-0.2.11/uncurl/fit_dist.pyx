# implementation of some distribution selection methods

#import cython
cimport cython

import numpy as np
cimport numpy as np

from libc.math cimport log2, log

from scipy import sparse
from scipy.special import xlogy

from scipy.stats import poisson
from scipy.stats import norm

ctypedef fused int2:
    short
    int
    long
    long long

ctypedef fused index_t:
    int
    long

ctypedef fused numeric:
    int
    long
    float
    double

def data2cdf(np.ndarray[numeric, ndim=1] data_array):
    """
    Converts a data array to a cdf...
    """
    numeric max_val = data_array.max()
    int[:] counts = np.array(int(round(max_val)))
    # TODO

def fit_errors(np.ndarray[int2, ndim=1] data_array):
    """
    Given a 1d array of integers, this returns a dict containing the fit
    errors for poiss, norm, and lognorm
    """
    np.ndarray[numeric, ndim=1] log_data = np.log(1 + data_array)
    int2[:] data_ = data_array
    numeric[:] log_data_ = log_data
    int2 data_max = data_array.max()
    numeric m = np.mean(data_array)
    numeric std = np.std(data_array, ddof=1)
    numeric m_l = np.mean(log_data)
    numeric std_l = np.std(log_data, ddof=1)
    int n_bins = min(50, data.max())
    np.ndarray[numeric, ndim=1] bins
    np.ndarray[numeric, ndim=1] edges
    if n_bins == 50:
        bin_counts, edges = np.histogram(data_array)
    int i = 0
    for i in range(0, n_bins):
        pass
    pass

def fit_errors_histogram(np.ndarray[int2, ndim=1] data_array):
    pass

def fit_errors_all(np.ndarray[int2, ndim=2] data_array):
    """
    """

def fit_errors_all_csr(np.ndarray[int2, ndim=1] data,
        np.ndarray[index_t, ndim=1] indices,
        np.ndarray[index_t, ndim=1] indptr):
    """
    Returns fit errors for a CSR matrix
    """
    np.ndarray[numeric, ndim=1] log_data = np.log(1 + data)
