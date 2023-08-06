import warnings
from inspect import signature

import numpy
import pandas
import datetime
from scipy.optimize import minimize
from scipy.signal import convolve
from scipy.stats import pearsonr

from . import constants
from .empirical_pval import compute_empirical_pvalue, compute_empirical_quantile, compute_p_confidence
from .utilities import rms_error
from .utilities import validate_param, log_print

DEBUG = False


class EmpiricalDistribution:
    _BIN_OFFSET = -1

    def __init__(self, frequencies, support):
        assert support[1] >= support[0]

        self.a, self.b = support  # ToDo: Add setter methods to a and b properties to do type-checking
        self.num_bins = len(frequencies)

        self._frequencies = numpy.array(frequencies)
        self._cdf_values = numpy.cumsum(self._frequencies)
        self._sf_values = numpy.cumsum(self._frequencies[::-1])[
                          ::-1]  # Double reversal needed to avoid numerical round-off errors close to 1.

    @staticmethod
    def fit(data, bins=constants.DEFAULT_BINS, pseudocount=constants.DEFAULT_PSEUDOCOUNT):
        data = numpy.array(data)
        assert len(data) > 0, 'Data must have non-zero length'
        counts, bins = numpy.histogram(data, bins=bins)
        support = bins[0], bins[-1]
        counts += pseudocount
        frequencies = counts / counts.sum()

        # ToDo: return a tuple instead of a dictionary
        return {'support': support, 'frequencies': frequencies}

    @classmethod
    def from_data(cls, data, bins=constants.DEFAULT_BINS, pseudocount=0):
        return cls(**cls.fit(data=data, bins=bins, pseudocount=pseudocount))

    @property
    def frequencies(self):
        return pandas.Series(self._frequencies, index=self.bin_starts)

    @property
    def densities(self):
        return pandas.Series(self._frequencies / self.bin_size, index=self.bin_midpoints)

    @property
    def cdf_series(self):
        return pandas.Series(self._cdf_values, index=self.bin_midpoints)

    @property
    def support_size(self):
        return self.b - self.a

    @property
    def support(self):
        return self.a, self.b

    @property
    def bin_size(self):
        return (self.b - self.a) / self.num_bins

    @property
    def bin_starts(self):
        return numpy.linspace(self.a, self.b - self.bin_size, num=self.num_bins)

    @property
    def bin_midpoints(self):
        return self.bin_starts + self.bin_size / 2

    @property
    def bin_ends(self):
        return self.bin_starts + self.bin_size

    def __neg__(self):
        return type(self)(frequencies=self._frequencies[::-1], support=(-self.b, -self.a))

    def __add__(self, other):
        try:  # assume other is another EmpiricalDistribution
            new_frequencies = convolve(other.frequencies, self._frequencies, mode='full',
                                       method=constants.CONVOLVE_METHOD)
            new_a = self.a + other.a
            new_b = self.b + other.b
            result = type(self)(frequencies=new_frequencies, support=(new_a, new_b))

        except AttributeError:  # if not, treat it as a scalar
            result = self.copy()
            result.a += other
            result.b += other

        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return -self.__add__(other)

    def __mul__(self, other):
        # Currently only supports scalars, multiplication by other distributions not implemented yet.
        result = self.copy()
        result.a = self.a * other
        result.b = self.b * other
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        # Currently only supports scalars, division by other distributions not implemented yet.
        result = self.copy()
        result.a = self.a / other
        result.b = self.b / other
        return result

    def copy(self):
        return type(self)(frequencies=self._frequencies, support=self.support)

    def mean(self):
        """
        Returns the expectation of the random variable described by this distribution
        """
        return numpy.sum(self._frequencies * self.bin_midpoints)

    def std(self):
        """
        Returns the standard deviation of the random variable described by this distribution
        """
        m = self.mean()
        return numpy.sqrt((((self.bin_midpoints - m) ** 2) * self.frequencies).sum())

    def resample(self, new_num_bins):
        """
        Return a copy where the frequencies have been re-sampled into :param new_num_bins: number of bins.
        """
        new_frequencies = numpy.interp(x=numpy.linspace(*self.support, new_num_bins),
                                       xp=numpy.linspace(*self.support, self.num_bins), fp=self.frequencies)
        new_frequencies /= new_frequencies.sum()

        return type(self)(frequencies=new_frequencies, support=self.support)

    def pdf(self, x):
        """
        Returns the PDF evaluated at the points in :param:`x`
        as the density of the overlapping bins.
        """
        freq_array = self._frequencies
        return freq_array[numpy.maximum(0, numpy.searchsorted(self.bin_starts, x) + self._BIN_OFFSET)] / self.bin_size

    def cdf(self, x):
        """
        Returns the CDF evaluated at the points in :param:`x`
        """
        return numpy.maximum(self._cdf_values[numpy.maximum(0, numpy.searchsorted(self.bin_starts, x) + self._BIN_OFFSET)], constants.MIN_PVALUE)

    def sf(self, x):
        """
        Return the survival function (1 - cdf) at :param x:
        """
        return numpy.maximum(self._sf_values[numpy.maximum(0, numpy.searchsorted(self.bin_starts, x) + self._BIN_OFFSET)], constants.MIN_PVALUE)

    def isf(self, x):
        """
        Return the inverse survival function (1 - sf) at :param x:
        """
        return 1 - self.sf(x)

    def logsf(self, x):
        # ToDo: Build in standard approximation (should never return 0 p-values)
        return numpy.log(numpy.maximum(self.sf(x), constants.MIN_PVALUE))


# ToDo: Consider whether we even need this parent class anymore.
class _PiecewiseEmpiricalApprox:
    @classmethod
    def _compute_empirical_pvalues(cls, data, fit_range=None,
                                   tail='right',
                                   num_fit_points=constants.DEFAULT_NUM_FIT_POINTS,
                                   is_sorted=False):
        if not is_sorted:
            data = numpy.sort(data)

        validate_param('tail', tail, ('left', 'right'))

        xs = numpy.linspace(*fit_range, num=num_fit_points)
        pvalues = compute_empirical_pvalue(data, values=xs, tail=tail, is_sorted=True)

        return xs, pvalues
        
        
class _NoDistribution(_PiecewiseEmpiricalApprox):
    
    def __init__(self):
        """
        An "active nothing" class that returns empty arrays for all its methods
        """
        pass
        
    def pdf(self, x):
        return numpy.array([])

    def cdf(self, x):
        return numpy.array([])

    def sf(self, x):
        return numpy.array([])

    def logsf(self, x):
        return numpy.array([])

    def isf(self, x):
        return numpy.array([])        
        

class _GenericTail(_PiecewiseEmpiricalApprox):
    """
    """

    def __init__(self, distro_params, tail, distribution_class=constants.DEFAULT_TAIL_DISTRIBUTION):
        #         distro_params = params[:-2]
        #         tail = params[-2]
        #         distribution_class = params[]
        self.tail = tail
        self.frozen_rv = distribution_class(*distro_params)
        
    @staticmethod
    def _generate_obj_func_shape_penalized(target_xs, pvalues, distro_class, support_range,
                                           loc=0, scale=1,
                                           support_penalty=constants.DEFAULT_SUPPORT_PENALTY, support_penalty_scale=constants.DEFAULT_SUPPORT_PENALTY_SCALE):
        def obj_func(params):
            shapes = params
            test_distro = distro_class(*shapes, loc=loc, scale=scale)
            predicted_xs = test_distro.ppf(q=1 - pvalues)

            score = -pearsonr(target_xs, predicted_xs)[0]

            this_scale = target_xs.std() / predicted_xs.std()
            predicted_xs *= this_scale
            this_loc = target_xs.mean() - predicted_xs.mean()
            predicted_xs += this_loc
            
            scaled_distro = distro_class(*shapes, loc=this_loc, scale=this_scale)

            min_x = scaled_distro.ppf(0.0)
            max_x = scaled_distro.ppf(1.0)
            # print('max_support: {}, max x: {}, max_support sf: {}'.format(max_support, max_x, test_distro.sf(max_support)))
       
            if min_x > support_range[0]:
                score += support_penalty + support_penalty_scale * (min_x - support_range[0])
                if DEBUG:
                    log_print('{} < a:{}'.format(support_range[0], min_x),4)
                    
            if max_x < support_range[1]:
                score += support_penalty + support_penalty_scale * (support_range[1] - max_x)
                if DEBUG:
                    log_print('{} > b:{}'.format(support_range[1], max_x),4)
            #
            if DEBUG:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(1, figsize=(4, 3))
                ax.plot(target_xs, pvalues, label='true')
                ax.plot(predicted_xs, pvalues, label='predicted')
            
                ax.legend(loc=0)
                ax.set_title('score: {}, params: {}'.format(score, list(params) + [this_loc, this_scale]))
                plt.show()

            if numpy.isnan(score) or numpy.isneginf(score):
                return numpy.inf

            return score

        return obj_func    
    
    @staticmethod
    def _generate_obj_func_final_penalized(target_xs, pvalues, distro_class, support_range, support_penalty=constants.DEFAULT_SUPPORT_PENALTY,
                                           support_penalty_scale=constants.DEFAULT_SUPPORT_PENALTY_SCALE):
        def obj_func(params):
            test_distro = distro_class(*params)
            loc = params[-2]
            scale = params[-1]

            predicted_ys = test_distro.logsf(target_xs)

            score = rms_error(pvalues, predicted_ys)
            
            min_x = test_distro.ppf(0.0)
            max_x = test_distro.ppf(1.0)

            # print('params: {}'.format(params))
            # print('max_support: {}, max x: {}, max_support sf: {}'.formast(max_support, max_x, test_distro.sf(max_support)))

            if DEBUG:
                print('support_range: {}, min_x: {}, max_x: {}'.format(support_range, min_x, max_x), 4)
            
            if min_x > support_range[0]:
                score += support_penalty + support_penalty_scale * (min_x - support_range[0])
                if DEBUG:
                    log_print('{} < a:{}'.format(support_range[0], min_x),4)
                    
            if max_x < support_range[1]:
                score += support_penalty + support_penalty_scale * (support_range[1] - max_x)
                if DEBUG:
                    log_print('{} > b:{}'.format(support_range[1], max_x),4)
                                                 
            # if not test_distro.sf(max_support) > 0:
                # score += support_penalty
                # if DEBUG:
                    # log_print('Got 0 p-value for {}'.format(max_support),4)                    

            if DEBUG:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(1, figsize=(4, 3))
                ax.plot(target_xs, pvalues, label='true')
                ax.plot(target_xs, predicted_ys, label='predicted')
                ax.legend(loc=0)
                ax.set_title('score: {}, params: {}'.format(score, params))
                plt.show()

            if numpy.isnan(score) or numpy.isneginf(score):
                return numpy.inf

            return score

        return obj_func    

    @classmethod
    def _initial_fit(cls, target_xs, pvalues, distro_class, support_range, 
                    initial_shapes=None, support_penalty=constants.DEFAULT_SUPPORT_PENALTY,
                     support_penalty_scale=constants.DEFAULT_SUPPORT_PENALTY_SCALE):

        num_params = len(signature(distro_class._parse_args).parameters)
        #     start_time = datetime.datetime.now()

        if initial_shapes is None:
            initial_shapes = (numpy.full(num_params - 2, fill_value=constants.DEFAULT_SHAPE))
    
        if len(initial_shapes) > 0:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                initial_obj_func = cls._generate_obj_func_shape_penalized(target_xs, pvalues,
                                                                          distro_class=distro_class,
                                                                          support_range=support_range,
                                                                          support_penalty=support_penalty,
                                                                          support_penalty_scale=support_penalty_scale)

                res = minimize(fun=initial_obj_func, x0=initial_shapes,
                               method='Nelder-Mead',
                               options={'maxiter': 1000})

            shapes = res.x
            scaling_distro = distro_class(*shapes, loc=0, scale=1)
        else:
            shapes = []
            scaling_distro = distro_class(loc=0, scale=1)

        # obtain best-fit loc and scale
        scaling_xs = scaling_distro.ppf(1 - pvalues)

        scale = target_xs.std() / scaling_xs.std()
        scaling_xs *= scale
        loc = target_xs.mean() - scaling_xs.mean()
        #     elapsed_ms = (datetime.datetime.now() - start_time).microseconds / 1000

        return numpy.hstack((shapes, [loc, scale]))

    @classmethod
    def _final_fit(cls, target_xs, target_pvalues, distro_class, support_range, x0,
                   support_penalty=0.1, support_penalty_scale=1):
                   
        # print('starting final fit with parameters: {}'.format(x0))

        obj_func = cls._generate_obj_func_final_penalized(target_xs, numpy.log(target_pvalues), distro_class,
                                                          support_range=support_range,
                                                          support_penalty=support_penalty,
                                                          support_penalty_scale=support_penalty_scale)

        res = minimize(fun=obj_func, x0=x0, method='Nelder-Mead', options={'maxiter': constants.FIT_MAXITER,
                                                                           'xatol': constants.FIT_FATOL,
                                                                           'fatol': constants.FIT_XATOL})
        return res.x, res.fun, res.success

    @classmethod
    def fit_with_empirical_pvalues(cls, target_xs,
                                   target_pvalues,
                                   distro_class, support_range,
                                   initial_shapes=None,
                                   support_penalty=0.1, support_penalty_scale=1):

        start_time = datetime.datetime.now()
        # print('entering fit_with_empirical_pvalues')
        # print('fit range: {}, {}'.format(target_xs[0], target_xs[-1]))
        # print('support range: {}'.format(support_range))
        initial_params = cls._initial_fit(target_xs=target_xs, pvalues=target_pvalues,
                                          distro_class=distro_class,
                                          support_range=support_range,
                                          initial_shapes=initial_shapes,
                                          support_penalty=support_penalty, support_penalty_scale=support_penalty_scale)
        # print('*' * 80)
        # print('initial_params {}'.format(initial_params))
        final_params, final_error, final_success = cls._final_fit(target_xs=target_xs, target_pvalues=target_pvalues,
                                                                  distro_class=distro_class, support_range=support_range,
                                                                  x0=initial_params)

        elapsed_ms = (datetime.datetime.now() - start_time).microseconds / 1000
        # print('*' * 80)
        # print('final_params {}'.format(final_params))

        return {'params': final_params, 'success': final_success,
                'pos_score': final_error,
                'score_name': 'rms logsf error',
                'elapsed_ms': elapsed_ms}

    @classmethod
    def informative_fit(cls, data,
                        tail,
                        distro_class=constants.DEFAULT_TAIL_DISTRIBUTION,
                        support_range=None,
                        fit_range=None,
                        initial_shapes=None,
                        is_sorted=False,
                        num_fit_points=constants.DEFAULT_NUM_FIT_POINTS):

        # ToDo: replace with call to validate_param
        assert tail in (
            'left',
            'right'), 'Invalid value {} received for parameter "tail". Must be either "left" or "right".'.format(
            tail)

        if not is_sorted:
            data = numpy.sort(data)
            
        # print('informative fit support range: {}, fit range: {}'.format(support_range, fit_range))

        if fit_range is None:
            fit_range = data[0], data[-1]

        if support_range is None:
            support_range = data[0], data[-1]

        target_xs, pvalues = cls._compute_empirical_pvalues(data, fit_range=fit_range, tail=tail,
                                                            num_fit_points=num_fit_points,
                                                            is_sorted=True)

        if tail == 'left':
            target_xs = -target_xs
            support_range = -fit_range[1], -support_range[0]
        else:
            support_range = fit_range[1], support_range[1]

        fit_result = cls.fit_with_empirical_pvalues(target_xs, pvalues,
                                                    initial_shapes=initial_shapes,
                                                    distro_class=distro_class,
                                                    support_range=support_range)

        fit_result['params'] = (fit_result['params'], tail, distro_class)
        return fit_result

    @classmethod
    def fit(cls,
            data,
            tail,
            distro_class=constants.DEFAULT_TAIL_DISTRIBUTION,
            support_range=None,
            fit_range=None,
            is_sorted=False,
            num_fit_points=constants.DEFAULT_NUM_FIT_POINTS):

        fit_result = cls.informative_fit(data=data,
                                         tail=tail,
                                         distro_class=distro_class,
                                         fit_range=fit_range,
                                         support_range=support_range,
                                         is_sorted=is_sorted,
                                         num_fit_points=num_fit_points)

        # only return parameters (mimic the signature of scipy rv fit methods)
        return fit_result['params']

    def pdf(self, xs):
        if self.tail == 'left':
            return self.frozen_rv.pdf(-xs)
        else:
            return self.frozen_rv.pdf(xs)

    def cdf(self, xs):
        if self.tail == 'left':
            return self.frozen_rv.sf(-xs)
        else:
            return self.frozen_rv.cdf(xs)

    def sf(self, xs):
        if self.tail == 'left':
            return self.frozen_rv.cdf(-xs)
        else:
            return self.frozen_rv.sf(xs)

    def logsf(self, xs):
        return numpy.log(self.frozen_rv.sf(xs))


class HybridDistribution(_PiecewiseEmpiricalApprox):
    """
    """

    def __init__(self, center_frozen_rv, left_tail_frozen_rv, left_crossover_point, right_tail_frozen_rv,
                 right_crossover_point):
        self.left_crossover_point = left_crossover_point
        self.right_crossover_point = right_crossover_point
        self.center_frozen_rv = center_frozen_rv
        self.left_tail_frozen_rv = left_tail_frozen_rv
        self.right_tail_frozen_rv = right_tail_frozen_rv

    @classmethod
    def informative_fit(cls, data,
                        support_range=None,
                        unique_samples=0,
                        is_sorted=False,
                        tail_quantile_cutoff=constants.DEFAULT_TAIL_QUANTILE_CUTOFF,
                        max_pvalue_cv=constants.DEFAULT_MAX_PVALUE_CV,
                        center_distribution_class=EmpiricalDistribution,
                        tail_distribution_class=_GenericTail,
                        num_fit_points=constants.DEFAULT_NUM_FIT_POINTS,
                        bins=constants.DEFAULT_BINS,
                        log_message_indentation=0):
        """
        Basic idea is to fit genpareto tail to the portion of the data that falls between the
        max pvalue and the max confident x value, and then that max confident x value becomes our
        crossover point. We will generate a histogram-based EmpiricalDistribution for that same
        data range. Queries between the crossover points will be answered from the EmpiricalDistribution,
        and queries outside the crossover points will come from the genpareto tails.
        """
        # ToDo Clean up flow control
        if not is_sorted:
            data = numpy.sort(data)

        if not unique_samples:
            unique_samples = len(data)

        if support_range is None:
            log_print('no explicit support range specified, inferring from data', log_message_indentation)
            support_range = numpy.min(data), numpy.max(data)

        log_print('require support: [{},{}]'.format(*support_range), log_message_indentation)
        # fit_tails = True

        log_print('fitting center ...', log_message_indentation)
        # print(numpy.isnan(data).sum(), numpy.isinf(data).sum(), numpy.isneginf(data).sum())
        center_frozen_rv = center_distribution_class.from_data(data, bins=bins)

        # Compute crossover points
        best_confident_pvalue = compute_p_confidence(n=unique_samples, pvalue_cv=max_pvalue_cv)

        left_tail_x_start = compute_empirical_quantile(data, tail_quantile_cutoff,
                                                       is_sorted=True)
        left_tail_x_end = compute_empirical_quantile(data, best_confident_pvalue,
                                                     is_sorted=True)

        right_tail_x_start = compute_empirical_quantile(data, 1 - tail_quantile_cutoff,
                                                        is_sorted=True)
        right_tail_x_end = compute_empirical_quantile(data, 1 - best_confident_pvalue,
                                                      is_sorted=True)

        # ToDo throw custom exceptions, clean up flow control
        if not best_confident_pvalue < tail_quantile_cutoff:
            log_print(
                'With {} samples ({} unique, the smallest p-value we can compute at a < {} CV is {}. However, this is greater than {}, start p-value of the tail approximation. Therefore no tail approximations will be fit.'.format(
                    len(data), unique_samples, max_pvalue_cv, best_confident_pvalue, tail_quantile_cutoff),
                log_message_indentation)

            left_tail_frozen_rv = _NoDistribution()
            left_crossover_point = -numpy.infty
            right_tail_frozen_rv = _NoDistribution()
            right_crossover_point = numpy.infty

        else:

            log_print('fitting left tail to data in range ({},{}) ...'.format(left_tail_x_start, left_tail_x_end),
                      log_message_indentation, continue_line=True)

            left_tail_distro_result = tail_distribution_class.informative_fit(data, tail='left',
                                                                              fit_range=(
                                                                                  left_tail_x_end, left_tail_x_start),
                                                                               support_range=support_range,
                                                                              num_fit_points=num_fit_points,
                                                                              is_sorted=True
                                                                              )
            log_print(
                ' {}, achieving {} of {}'.format(
                    ['FAILED', 'SUCCEEDED'][left_tail_distro_result['success']],
                    left_tail_distro_result['score_name'],
                    left_tail_distro_result['pos_score']),
                log_message_indentation)

            if left_tail_distro_result['success']:
                left_tail_frozen_rv = tail_distribution_class(*left_tail_distro_result['params'])
                left_crossover_point = left_tail_x_end
            else:
                left_tail_frozen_rv = _NoDistribution()
                left_crossover_point = -numpy.infty

            log_print('fitting right tail to data in range ({},{}) ...'.format(right_tail_x_start, right_tail_x_end),
                      log_message_indentation, continue_line=True)
            right_tail_distro_result = tail_distribution_class.informative_fit(data, tail='right',
                                                                               fit_range=(
                                                                                   right_tail_x_start,
                                                                                   right_tail_x_end),
                                                                               support_range=support_range,
                                                                               num_fit_points=num_fit_points,
                                                                               #                                                                       optimization_kwargs=optimization_kwargs,
                                                                               is_sorted=True
                                                                               )
            log_print(
                ' {}, achieving {} of {}'.format(
                    ['FAILED', 'SUCCEEDED'][right_tail_distro_result['success']],
                    right_tail_distro_result['score_name'],
                    right_tail_distro_result['pos_score']),
                log_message_indentation)

            if right_tail_distro_result['success']:
                right_tail_frozen_rv = tail_distribution_class(*right_tail_distro_result['params'])
                right_crossover_point = right_tail_x_end
            else:
                right_tail_frozen_rv = _NoDistribution()
                right_crossover_point = numpy.infty

        params = [center_frozen_rv, left_tail_frozen_rv, left_crossover_point, right_tail_frozen_rv, right_crossover_point]

        return {'params': params}  # Todo: figure out what other info we want to pass back up.

    @classmethod
    def fit(cls, data,
            support_range=None,
            unique_samples=0, is_sorted=False,
            center_distribution_class=EmpiricalDistribution,
            tail_distribution_class=_GenericTail,
            tail_quantile_cutoff=constants.DEFAULT_TAIL_QUANTILE_CUTOFF,
            max_pvalue_cv=constants.DEFAULT_MAX_PVALUE_CV,
            num_fit_points=constants.DEFAULT_NUM_FIT_POINTS,
            bins=constants.DEFAULT_BINS,
            ):
        """
        Basic idea is to fit genpareto tail to the portion of the data that falls between the
        max pvalue and the max confident x value, and then that max confident x value becomes our
        crossover point. We will generate a histogram-based EmpiricalDistribution for that same
        data range. Queries between the crossover points will be answered from the EmpiricalDistribution,
        and queries outside the crossover points will come from the genpareto tails.
        """
        # ToDo: consider setting all additional arguments to their defaults so that .fit() signature matches scipy rvs.
        # print('fit_method received support [{},{}'.format(min_support, max_support))
        fit_results = cls.informative_fit(data=data,
                                          support_range=support_range,
                                          unique_samples=unique_samples, is_sorted=is_sorted,
                                          center_distribution_class=center_distribution_class,
                                          tail_distribution_class=tail_distribution_class,
                                          tail_quantile_cutoff=tail_quantile_cutoff,
                                          max_pvalue_cv=max_pvalue_cv,
                                          num_fit_points=num_fit_points,
                                          bins=bins,
                                          log_message_indentation=0)
        return fit_results['params']

    def _partition_x(self, x):
        """
        Returns 3 arrays of indices of x: values for the left tail,
        values for the center and values for the right tail.
        """
        in_left_tail = x < self.left_crossover_point
        in_right_tail = x > self.right_crossover_point
        in_center = numpy.logical_not(numpy.logical_or(in_left_tail, in_right_tail))
        
        return numpy.nonzero(in_left_tail), numpy.nonzero(in_center), numpy.nonzero(in_right_tail)
        
    #ToDo: improve handling of arrays vs. scalars in these methods
    def pdf(self, x):
        x = numpy.array(x)
        left_x_indices, center_x_indices, right_x_indices = self._partition_x(x)
        result = numpy.empty(len(x))
        result[left_x_indices] = self.left_tail_frozen_rv.pdf(x[left_x_indices])
        result[center_x_indices] = self.center_frozen_rv.pdf(x[center_x_indices])
        result[right_x_indices] = self.right_tail_frozen_rv.pdf(x[right_x_indices])
        return result

    def cdf(self, x):
        x = numpy.array(x)    
        left_x_indices, center_x_indices, right_x_indices = self._partition_x(x)
        result = numpy.empty(len(x))
        result[left_x_indices] = self.left_tail_frozen_rv.cdf(x[left_x_indices])
        result[center_x_indices] = self.center_frozen_rv.cdf(x[center_x_indices])
        result[right_x_indices] = self.center_frozen_rv.cdf(x[right_x_indices])
        return result

    def sf(self, x):
        x = numpy.array(x)
        left_x_indices, center_x_indices, right_x_indices = self._partition_x(x)
        result = numpy.empty(len(x))
        result[left_x_indices] = self.center_frozen_rv.sf(x[left_x_indices])
        result[center_x_indices] = self.center_frozen_rv.sf(x[center_x_indices])
        result[right_x_indices] = self.right_tail_frozen_rv.sf(x[right_x_indices])
        return result
        
    def logsf(self, x):
        x = numpy.array(x)
        left_x_indices, center_x_indices, right_x_indices = self._partition_x(x)
        result = numpy.empty(len(x))   
        result[left_x_indices] = self.center_frozen_rv.logsf(x[left_x_indices])
        result[center_x_indices] = self.center_frozen_rv.logsf(x[center_x_indices])
        result[right_x_indices] = self.right_tail_frozen_rv.logsf(x[right_x_indices])
        return result        
