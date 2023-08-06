import scipy.stats

from .external_operators import minimum_distribution, maximum_distribution


def predict_distributions_independent_sums(input_empirical_distribution,
                                           max_sample_size):
    """
    Given an EmpiricalDistribution instance generated from a population sample, return a dictionary,
    keyed by sample size, of EmpiricalDistribution instances representing the expected distributions
    of the sum of samples taken from that population of sizes [1, :param:`max_sample_size`].

    :param input_empirical_distribution:
    :param max_sample_size:
    :return:
    """

    assert max_sample_size >= 1

    empirical_distros_by_region_size = {1: input_empirical_distribution}

    for sample_size in range(2, max_sample_size + 1):
        empirical_distros_by_region_size[sample_size] = empirical_distros_by_region_size[
                                                            sample_size - 1] + input_empirical_distribution

    return empirical_distros_by_region_size


def predict_distributions_independent_means(input_empirical_distribution,
                                            max_sample_size):
    """
    Given an EmpiricalDistribution instance generated from a population sample, return a dictionary,
    keyed by sample size, of EmpiricalDistribution instances representing the expected distributions
    of the mean of samples taken from that population of sizes [1, :param:`max_sample_size`].

    :param input_empirical_distribution:
    :param max_sample_size:
    :return:
    """
    assert max_sample_size >= 1

    sum_distributions = predict_distributions_independent_sums(
        input_empirical_distribution=input_empirical_distribution, max_sample_size=max_sample_size)

    return {sample_size: distribution / sample_size for sample_size, distribution in sum_distributions.items()}


def predict_distributions_independent_mins(input_empirical_distribution,
                                           max_sample_size):
    """
    Given an EmpiricalDistribution instance generated from a population sample, return a dictionary,
    keyed by sample size, of EmpiricalDistribution instances representing the expected distributions
    of the minimum of samples taken from that population of sizes [1, :param:`max_sample_size`].

    :param input_empirical_distribution:
    :param max_sample_size:
    :return:
    """
    assert max_sample_size >= 1

    empirical_distros_by_region_size = {1: input_empirical_distribution}

    for sample_size in range(2, max_sample_size + 1):
        empirical_distros_by_region_size[sample_size] = minimum_distribution(empirical_distros_by_region_size[
                                                                                 sample_size - 1],
                                                                             input_empirical_distribution)

    return empirical_distros_by_region_size


def predict_distributions_independent_maxes(input_empirical_distribution,
                                            max_sample_size):
    """
    Given an EmpiricalDistribution instance generated from a population sample, return a dictionary,
    keyed by sample size, of EmpiricalDistribution instances representing the expected distributions
    of the maximum of samples taken from that population of sizes [1, :param:`max_sample_size`].

    :param input_empirical_distribution:
    :param max_sample_size:
    :return:
    """
    assert max_sample_size >= 1

    empirical_distros_by_region_size = {1: input_empirical_distribution}

    for sample_size in range(2, max_sample_size + 1):
        empirical_distros_by_region_size[sample_size] = maximum_distribution(empirical_distros_by_region_size[
                                                                                 sample_size - 1],
                                                                             input_empirical_distribution)

    return empirical_distros_by_region_size


def compute_expected_unique_samples(total_items, num_samples):
    """
    Return the expected number of unique items from a set of size :param total_items:
    in a sample of size :param num_samples: with replacement.
    """
    unsampled_items = scipy.stats.binom(num_samples, 1/total_items).pmf(0)
    if unsampled_items < 1.0:
        return int((1 - unsampled_items) * total_items)
    else:
        return num_samples
