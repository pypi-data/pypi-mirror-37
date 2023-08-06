import numpy

from .empirical_distributions import EmpiricalDistribution
from .constants import RESAMPLE_FACTOR
from .utilities import cdf_to_pdf


#ToDo: Refactor these back to match the old EmpricialDistribution interface.
def minimum_distribution(distro_1, distro_2):
    """
    Given two EmpiricalDistribution instances, return an EmpiricalDistribution instance containing the expected
    distribution of an element-wise minimum operation between the *independent* random variables modeled by the input
    distributions.


    :param distro_1:
    :param distro_2:
    :return:
    """
    if len(distro_1._hbins) == len(distro_2._hbins) and not numpy.abs(distro_1._hbins - distro_2._hbins).sum() > 0:
        new_a, new_b = distro_1.a, distro_1.b
        new_num_bins = len(distro_1._hbins)
        common_bins = distro_1._hbins + distro_1._hbins
    else:
        new_a, new_b = min(distro_1.a, distro_2.a), min(distro_1.b, distro_2.b)
        new_num_bins = int(numpy.ceil((len(distro_1._hbins) + len(distro_2._hbins)) * RESAMPLE_FACTOR))
        new_bin_width = (new_b - new_a) / (new_num_bins - 1)
        common_bins = numpy.linspace(new_a, new_b+new_bin_width, num=new_num_bins)

    pred_cdf = distro_1.cdf(common_bins) + distro_2.cdf(common_bins) - (
            distro_1.cdf(common_bins) * distro_2.cdf(common_bins))
    pred_pdf = cdf_to_pdf(pred_cdf)

    return EmpiricalDistribution(histogram=(pred_pdf[1:],
                                            common_bins))


def maximum_distribution(distro_1, distro_2):
    """
    Given two EmpiricalDistribution instances, return an EmpiricalDistribution instance containing the expected
    distribution of an element-wise maximum operation between the *independent* random variables modeled by the input
    distributions.


    :param distro_1:
    :param distro_2:
    :return:
    """
    if len(distro_1._hbins) == len(distro_2._hbins) and not numpy.abs(distro_1._hbins - distro_2._hbins).sum() > 0:
        new_a, new_b = distro_1.a, distro_1.b
        new_num_bins = len(distro_1._hbins)
        common_bins = distro_1._hbins + distro_1._hbins
    else:
        new_a, new_b = max(distro_1.a, distro_2.a), max(distro_1.b, distro_2.b)
        new_num_bins = int(numpy.ceil((len(distro_1._hbins) + len(distro_2._hbins)) * RESAMPLE_FACTOR))
        new_bin_width = (new_b - new_a) / (new_num_bins - 1)
        common_bins = numpy.linspace(new_a, new_b+new_bin_width, num=new_num_bins)

    pred_cdf = distro_1.cdf(common_bins) * distro_2.cdf(common_bins)
    pred_pdf = cdf_to_pdf(pred_cdf)

    return EmpiricalDistribution(histogram=(pred_pdf[1:],
                                            common_bins))
