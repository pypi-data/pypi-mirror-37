import warnings

import numpy
from scipy.optimize import fmin
from scipy.signal import convolve
from scipy.stats import rv_histogram, genpareto, pearsonr

from . import constants
from .empirical_pval import compute_empirical_pvalue, compute_empirical_quantile, compute_p_confidence
from .utilities import validate_param, log_print


class EmpiricalDistributionWrapper(rv_histogram):
    @staticmethod
    def _convert_pdf_to_histogram_counts(hpdf):
        """
        Strips off the first and last value of the PDF array :param `hpdf`: in order
        to use it as a simulated histogram count array that will accepted by the
        constructor.
        """
        return hpdf[1:-1]

    @staticmethod
    def _generate_bins(a, b, num_bins):
        assert b > a
        bin_width = (b - a) / num_bins
        return numpy.linspace(a, b + bin_width, num=num_bins + 1)

    @classmethod
    def from_data(cls, data, bins='auto'):
        return cls(histogram=numpy.histogram(data, bins=bins))

    def __neg__(self):
        return type(self)(histogram=(self._convert_pdf_to_histogram_counts(self._hpdf[::-1]), -self._hbins[::-1]))

    def __add__(self, other):
        try:  # assume other is another improved_rv_histogram
            new_counts = convolve(other._hpdf, self._hpdf, mode='full', method=constants.CONVOLVE_METHOD)
            new_a = self.a + other.a
            new_b = self.b + other.b

        except AttributeError:  # if not, treat it as a scalar
            new_counts = self._convert_pdf_to_histogram_counts(self._hpdf)
            new_a = self.a + other
            new_b = self.b + other

        new_bins = self._generate_bins(new_a, new_b, len(new_counts))
        return type(self)(histogram=(new_counts, new_bins))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return -self.__add__(other)

    def __mul__(self, other):
        # Currently only supports scalars, multiplication by other distributions not implemented yet.
        new_counts = self._convert_pdf_to_histogram_counts(self._hpdf)
        new_a = self.a * other
        new_b = self.b * other

        new_bins = self._generate_bins(new_a, new_b, len(new_counts))
        return type(self)(histogram=(new_counts, new_bins))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        # Currently only supports scalars, multiplication by other distributions not implemented yet.
        new_counts = self._convert_pdf_to_histogram_counts(self._hpdf)
        new_a = self.a / other
        new_b = self.b / other

        new_bins = self._generate_bins(new_a, new_b, len(new_counts))
        return type(self)(histogram=(new_counts, new_bins))

    def copy(self):
        return type(self)(histogram=(self._convert_pdf_to_histogram_counts(self._hpdf), self._hbins))

    def resample(self, new_num_bins):
        """
        Return a copy where the frequencies have been re-sampled into :param new_num_bins: number of bins.
        """
        new_counts = numpy.interp(x=numpy.linspace(self.a, self.b, new_num_bins),
                                  xp=self._hbins, fp=self._hpdf[1:])
        new_bins = self._generate_bins(self.a, self.b, new_num_bins)
        return type(self)(histogram=(new_counts, new_bins))


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


class _GenericTail(_PiecewiseEmpiricalApprox):
    """
    """

    def __init__(self, distro_params, tail, distribution_class=constants.DEFAULT_TAIL_DISTRIBUTION):
#         distro_params = params[:-2]
#         tail = params[-2]
#         distribution_class = params[]
        self.tail = tail
        self.frozen_rv = distribution_class(*distro_params)

    @classmethod
    def _inital_fit(cls, target_xs, pvalues, distro_class, max_support, default_shape=1, support_penalty=0.1, support_penalty_scale=1):

        num_params = len(signature(distro_class._parse_args).parameters)
    #     start_time = datetime.datetime.now()

        shape_x0 = (numpy.full(num_params-2, fill_value=DEFAULT_SHAPE))
        if len(shape_x0) > 0:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                initial_obj_func= cls._generate_obj_func_shape_penalized(smallscale_xs, smallscale_ps, 
                                                         distro_class=distro_class,
                                                        max_support=max_support,
                                                                    support_penalty=support_penalty,
                                                                    support_penalty_scale=support_penalty_scale)

                res = scipy.optimize.minimize(fun=initial_obj_func, x0=shape_x0, 
                                              method='Nelder-Mead',
                                              options={'maxiter':1000})


            shapes = res.x
            scaling_distro = distro_class(*shapes, loc=0, scale=1)
        else:
            shapes=[]
            scaling_distro = distro_class(loc=0, scale=1)

        # obtain best-fit loc and scale
        scaling_xs = scaling_distro.ppf(1 - pvalues)

        scale = target_xs.std() / scaling_xs.std()
        scaling_xs *= scale
        loc = target_xs.mean() - scaling_xs.mean()
    #     elapsed_ms = (datetime.datetime.now() - start_time).microseconds / 1000

        return numpy.hstack((shapes, [loc, scale]))

    @classmethod
    def _final_fit(cls, target_xs, target_pvalues, distro_class, max_support, x0, 
                  support_penalty=0.1, support_penalty_scale=1):

        obj_func = cls._generate_obj_func_final_penalized(target_xs, numpy.log(target_pvalues), distro_class, 
                                              max_support=max_support, 
                                              support_penalty=support_penalty,
                                              support_penalty_scale=support_penalty_scale)

        res = scipy.optimize.minimize(fun=obj_func, x0=x0, method='Nelder-Mead', options={'maxiter':1000,
                                                                                                     'xatol':0.000001,
                                                                                                     'fatol':0.000001})
        return res.x, res.fun, res.success
    
    @classmethod
    def fit_with_empirical_pvalues(cls, target_xs,
                                   target_pvalues,
                                   distro_class, max_support, 
                                   default_shape=1,
                                   support_penalty=0.1, support_penalty_scale=1):
        
        start_time = datetime.datetime.now()
        initial_params = cls._inital_fit(target_xs=target_xs, pvalues=target_pvalues,
                                   distro_class=distro_class,
                                   max_support=max_support,
                                   default_shape=default_shape, 
                                   support_penalty=support_penalty, support_penalty_scale=support_penalty_scale)
        print('*'*80)
        print('initial_params {}'.format(initial_params))
        final_params, final_error, final_success = cls._final_fit(target_xs=target_xs, target_pvalues=target_pvalues, 
                                 distro_class=distro_class, max_support=max_support,
                                 x0=initial_params)

        elapsed_ms = (datetime.datetime.now() - start_time).microseconds / 1000
        print('*'*80)
        print('final_params {}'.format(final_params))  

        return {'params': final_params, 'success': final_success, 
                'pos_score': final_error, 
                'score_name': 'rms logsf error',
                'elapsed_ms':elapsed_ms}

    @classmethod
    def informative_fit(cls, data,
                        tail,
                        distro_class=constants.DEFAULT_TAIL_DISTRIBUTION,
                        max_support=None,
                        fit_range=None,
                        is_sorted=False,
                        num_fit_points=constants.DEFAULT_NUM_FIT_POINTS):
        
        # ToDo: replace with call to validate_param
        assert tail in (
            'left',
            'right'), 'Invalid value {} received for parameter "tail". Must be either "left" or "right".'.format(
            tail)

        if not is_sorted:
            data = numpy.sort(data)

        if fit_range is None:
            fit_range = data[0], data[-1]

        if max_support is None:
            max_support = fit_range[1]
            
        target_xs, pvalues = cls._compute_empirical_pvalues(data, fit_range=fit_range, tail=tail,
                                                            num_fit_points=num_fit_points, 
                                                            is_sorted=True)

        if tail == 'left':
            target_xs = -target_xs
            max_support = -max_support
        
        fit_result = cls.fit_with_empirical_pvalues(target_xs, pvalues,
                                                    distro_class=distro_class,
                                                    max_support=max_support)
        
        fit_result['params'] = (fit_result['params'], tail, distro_class)
        return fit_result

    @classmethod
    def fit(cls,
            data,
            tail,
            distro_class=constants.DEFAULT_TAIL_DISTRIBUTION,
            max_support=None,
            fit_range=None,
            is_sorted=False,
            num_fit_points=constants.DEFAULT_NUM_FIT_POINTS):

        fit_result = cls.informative_fit(data=data,
                                         tail=tail,
                                         distro_class=distro_class,
                                         fit_range=fit_range,
                                         max_support=max_support,
                                         is_sorted=is_sorted,
                                         num_fit_points=num_fit_points)

        # only return parameters (mimic the signature of scipy rv fit methods)
        return fit_result['params']

    @staticmethod
    def _generate_obj_func_final_penalized(target_xs, pvalues, distro_class, max_support, support_penalty=0.1, support_penalty_scale=1):
        def obj_func(params):
            test_distro = distro_class(*params)
            loc = params[-2]
            scale = params[-1]

            predicted_ys = test_distro.logsf(target_xs)

            score = rms_error(pvalues, predicted_ys)

            true_b = (test_distro.b * scale) - loc
            support_exceedance = numpy.max(max_support - true_b, 0)
            if max_support >= true_b:
                score += support_penalty + support_penalty_scale * support_exceedance / (target_xs[-1] - target_xs[0])
                if DEBUG: 
                    print('{} > b:{}'.format(max_support,true_b))

            if DEBUG:
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

    @staticmethod
    def _generate_obj_func_shape_penalized(target_xs, pvalues, distro_class, max_support, 
                                           loc=0, scale=1, 
                                           support_penalty=0.1, support_penalty_scale=1):
        def obj_func(params):
            shapes = params
            test_distro = distro_class(*shapes, loc=loc, scale=scale)
            predicted_xs = test_distro.ppf(q=1 - pvalues)

            score = -pearsonr(target_xs, predicted_xs)[0]

            this_scale = target_xs.std() / predicted_xs.std()
            predicted_xs *= this_scale
            this_loc = target_xs.mean() - predicted_xs.mean()
            predicted_xs += this_loc

            true_b = (test_distro.b * this_scale) - this_loc

            support_exceedance = numpy.max(max_support - true_b, 0)

            if max_support >= true_b:
                score += support_penalty + support_penalty_scale * support_exceedance / (target_xs[-1] - target_xs[0])
                if DEBUG:
                    print('{} > b:{}'.format(max_support,true_b))

            if DEBUG:
                fig, ax = plt.subplots(1, figsize=(4, 3))
                ax.plot(target_xs, pvalues, label='true')
                ax.plot(predicted_xs, pvalues, label='predicted')

                ax.legend(loc=0)
                ax.set_title('score: {}, params: {}'.format(score, list(params) +[this_loc, this_scale]))
                plt.show()

            if numpy.isnan(score) or numpy.isneginf(score):
                return numpy.inf

            return score

        return obj_func

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
                        min_support=None,
                        max_support=None,
                        unique_samples=0,                         
                        is_sorted=False,
                        tail_quantile_cutoff=constants.DEFAULT_TAIL_QUANTILE_CUTOFF,
                        max_pvalue_cv=constants.DEFAULT_MAX_PVALUE_CV,
                        center_distribution_class=EmpiricalDistribution,
                        tail_distribution_class=_GenericTail,
                        num_fit_points=constants.DEFAULT_NUM_FIT_POINTS,
                        bins='auto',
#                         optimization_kwargs={},
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
            
        if min_support is None:
            min_support = numpy.min(data)
        if max_support is None:
            max_support = numpy.max(data)

        fit_tails = True

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

        # ToDo throw custom exceptions
        if not best_confident_pvalue < tail_quantile_cutoff:
            log_print(
                'With {} samples ({} unique, the smallest p-value we can compute at a < {} CV is {}. However, this is greater than {}, start p-value of the tail approximation. Therefore no tail approximations will be fit.'.format(
                    len(data), unique_samples, max_pvalue_cv, best_confident_pvalue, tail_quantile_cutoff),
                log_message_indentation)

            left_tail_frozen_rv = None
            right_tail_frozen_rv = None

        else:

            log_print('fitting left tail to data in range ({},{}) ...'.format(left_tail_x_start, left_tail_x_end),
                      log_message_indentation, continue_line=True)

            left_tail_distro_result = tail_distribution_class.informative_fit(data, tail='left',
                                                                     fit_range=(left_tail_x_end, left_tail_x_start),
                                                                              max_support=min_support,
                                                                     num_fit_points=num_fit_points,
#                                                                      optimization_kwargs=optimization_kwargs,
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
            else:
                left_tail_frozen_rv = None

            log_print('fitting right tail to data in range ({},{}) ...'.format(right_tail_x_start, right_tail_x_end),
                      log_message_indentation, continue_line=True)
            right_tail_distro_result = tail_distribution_class.informative_fit(data, tail='right',
                                                                      fit_range=(
                                                                      right_tail_x_start, right_tail_x_end),
                                                                               max_support=max_support,
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
            else:
                right_tail_frozen_rv = None

        params = [center_frozen_rv, left_tail_frozen_rv, left_tail_x_end, right_tail_frozen_rv, right_tail_x_end]

        return {'params': params}  # Todo: figure out what other info we want to pass back up.


    @classmethod
    def fit(cls, data,
            min_support=None,
            max_support=None,
            unique_samples=0, is_sorted=False,
            center_distribution_class = EmpiricalDistribution,
            tail_distribution_class=_GenericTail,            
            tail_quantile_cutoff=constants.DEFAULT_TAIL_QUANTILE_CUTOFF,
            max_pvalue_cv=constants.DEFAULT_MAX_PVALUE_CV,
            num_fit_points=constants.DEFAULT_NUM_FIT_POINTS,
            bins='auto',
            optimization_kwargs={}):
        """
        Basic idea is to fit genpareto tail to the portion of the data that falls between the
        max pvalue and the max confident x value, and then that max confident x value becomes our
        crossover point. We will generate a histogram-based EmpiricalDistribution for that same
        data range. Queries between the crossover points will be answered from the EmpiricalDistribution,
        and queries outside the crossover points will come from the genpareto tails.
        """
        # ToDo: consider setting all additional arguments to their defaults so that .fit() signature matches scipy rvs.
        fit_results = cls.informative_fit(data=data,
                                          min_support=min_support,
                                          max_support=max_support,
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
        if self.left_tail_frozen_rv is None:
            in_left_tail = numpy.full(len(x), fill_value=False, dtype=bool)
        else:
            in_left_tail = x < self.left_crossover_point

        if self.right_tail_frozen_rv is None:
            in_right_tail = numpy.full(len(x), fill_value=False, dtype=bool)
        else:
            in_right_tail = x > self.right_crossover_point

        in_center = numpy.logical_not(numpy.logical_or(in_left_tail, in_right_tail))

        return x[in_left_tail], x[in_center], x[in_right_tail]

    def logsf(self, x):
        left_x, center_x, right_x = self._partition_x(x)
        return numpy.hstack([self.left_tail_frozen_rv.logsf(left_x),
                             self.center_frozen_rv.logsf(center_x),
                             self.right_tail_frozen_rv.logsf(right_x)])

    def pdf(self, x):
        left_x, center_x, right_x = self._partition_x(x)
        return numpy.hstack([self.left_tail_frozen_rv.pdf(left_x),
                             self.center_frozen_rv.pdf(center_x),
                             self.right_tail_frozen_rv.pdf(right_x)])

    def cdf(self, x):
        left_x, center_x, right_x = self._partition_x(x)
        return numpy.hstack([self.left_tail_frozen_rv.cdf(left_x),
                             self.center_frozen_rv.cdf(center_x),
                             self.right_tail_frozen_rv.cdf(right_x)])

    def sf(self, x):
        left_x, center_x, right_x = self._partition_x(x)
        return numpy.hstack([self.left_tail_frozen_rv.sf(left_x),
                             self.center_frozen_rv.sf(center_x),
                             self.right_tail_frozen_rv.sf(right_x)])
