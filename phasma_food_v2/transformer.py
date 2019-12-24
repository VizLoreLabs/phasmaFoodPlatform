from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.neighbors import KernelDensity
import numpy as np
from scipy.signal import savgol_filter, convolve
from pywt import wavedec, downcoef
from scipy.interpolate import interp1d


class NonNeg(BaseEstimator, TransformerMixin):
    """Shift the values and set all negative values to zero."""

    def __init__(self, thres=0.):
        self.thres = thres

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        return np.maximum(0, x-self.thres)


class Selector(BaseEstimator, TransformerMixin):
    """Select a subset of the data's columns."""

    def __init__(self, mask):
        self.mask = mask

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        return x[:, self.mask]


class SavGol(BaseEstimator, TransformerMixin):

    def __init__(self, window_length, polyorder, savgol_args={}):
        """Apply Savitzky-Golay filter

        This transformer calls scipy.signal.savgol_filter.

        Parameters
        ----------

        window_length : int,
                        length of the window considered

        polyorder : int,
                    the order of the polynomial to fit

        savgol_args : dict,
                      additional parameters past to scipy.signal.savgol_filter

        """
        self.window_length = window_length
        self.polyorder = polyorder
        self.savgol_args = savgol_args

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        return savgol_filter(x, self.window_length, self.polyorder, **self.savgol_args)


class Detrend(BaseEstimator, TransformerMixin):

    def __init__(self, polyorder=2):
        """Fit a polynomial to each row and return the residual.

        Parameters
        ----------
        polyorder : int,
                    the order of the polynomial to fit, default=2

        """
        self.polyorder = polyorder

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x_obj = np.arange(x.shape[1])
        self.p_ = np.polyfit(x_obj, x.T, deg=self.polyorder, full=False)
        f = np.concatenate([np.polyval(self.p_[:, k], x).reshape((1, -1)) for k in range(self.p_.shape[1])], axis=0)
        return x-f


class DWT(BaseEstimator, TransformerMixin):

    def __init__(self, wavelet, level=None, mode='symmetric'):
        """Apply a discrete wavelet transform to each row

        This transformer calls pywt.wavedec

        Parameters
        ----------
        wavelet : str,
                  the wavelet to use

        level : None, int or dict with keys ['a', 'd'], values are lists of int
                if None, pywt.wavedec with maximum decomposition level is used
                if int, pywt.wavedec with the specified level is used
                if dict, approximation coefficients of levels specified under 'a'
                and detail coefficients of levels specified under 'd' are computed using pywt.downcoef

        mode : str,
               the treatment of the signal at the boundaries

        """
        self.wavelet = wavelet
        self.level = level
        self.mode = mode

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        res = []
        if type(self.level) == dict:
            for alevel in self.level['a']:
                res.append(np.concatenate([downcoef('a', x, wavelet=self.wavelet, mode=self.mode, level=alevel).reshape((1,-1)) for x in x], axis=0))
            for blevel in self.level['d']:
                res.append(np.concatenate([downcoef('d', x, wavelet=self.wavelet, mode=self.mode, level=blevel).reshape((1,-1)) for x in x], axis=0))
        else:
            res = wavedec(x, wavelet=self.wavelet, mode=self.mode, level=self.level, axis=-1)
        return np.concatenate(res, axis=-1)


class Interpolator(BaseEstimator, TransformerMixin):

    def __init__(self, n_points, kind='cubic'):
        """Spline interpolation of the data

        This transformer calls scipy.interpolate.interp1d

        Parameters
        ----------

        xnew : 1d-array,
               new point at which to evaluate the spline interpolation

        kind : str,
               the kind of interpolation (see scipy.interpolate.interp1d)

        """
        self.n_points = n_points
        self.kind = kind

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x_obj = np.arange(x.shape[1])
        xnew = np.linspace(0, x.shape[1], self.n_points)
        self.f_ = interp1d(x_obj, x, kind=self.kind)
        return self.f_(xnew)


class Conv(BaseEstimator, TransformerMixin):
    """Convolute the data with a kernel

    """

    def __init__(self, kernel, mode='same'):
        self.kernel = kernel
        self.mode = mode

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        return np.concatenate([convolve(x_obj, self.kernel, mode=self.mode).reshape((1, -1)) for x_obj in x], axis=0)


def _compute_bw(dists, factor=5, thres=1e-5):
    return np.maximum(thres, factor*(np.max(dists)-np.min(dists))/dists.shape[0])


class PCAres(BaseEstimator, TransformerMixin):

    def __init__(self, n_components=None, kd_params={}):
        self.n_components = n_components
        self.kd_params = kd_params

    def fit(self, X, y=None):
        self.PCA_ = PCA(n_components=self.n_components, whiten=False).fit(X, y)
        U = self.PCA_.transform(X)
        res_ssq = np.linalg.norm(X-U@self.PCA_.components_+self.PCA_.mean_, 2, axis=-1)**2
        bw = _compute_bw(res_ssq)
        self.KD_train_ = KernelDensity(bandwidth = bw, **self.kd_params).fit(res_ssq)
        return self

    def transform(self, X, y=None):
        U = self.PCA_.transform(X)
        res_ssq = np.linalg.norm(X-U@self.PCA_.components_+self.PCA_.mean_, 2, axis=-1)**2
        return self.KD_train.score_samples(res_ssq)



