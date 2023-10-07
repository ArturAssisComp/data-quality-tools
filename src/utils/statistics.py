

import numpy as np

def std_dev_weighted(weighted_dict:dict[int, int]):
    """
    Compute the standard deviation for a weighted distribution.

    Parameters:
    ----------
    weighted_dict : dict[int, int]
        A dictionary where keys represent data points and values represent their weights 
        (frequencies). The format is: key=data_point int, value=weight int.

    Returns:
    -------
    float
        The standard deviation of the weighted distribution.

    Notes:
    -----
    The function computes the weighted standard deviation without expanding the dataset. 
    This approach is memory efficient, especially for distributions with large weights.

    Example:
    -------
    >>> distribution = {0:2, 1:5, 3:3}
    >>> std_dev_weighted(distribution)
    1.247219128924647

    """
    if not weighted_dict:
        raise ValueError('Invalid empty dict')

    keys = np.array(list(weighted_dict.keys()))
    values = np.array(list(weighted_dict.values()))
    if any(map(lambda x:x<0, keys)):
        raise ValueError('Invalid negative key')
    if any(map(lambda x:x<0, values)):
        raise ValueError('Invalid negative frequency')
    if sum(values) == 0:
        raise ValueError('Total frequency must not be 0')

    weighted_mean = np.average(keys, weights=values)

    variance = np.dot(values, (keys - weighted_mean)**2) / values.sum()
    
    return np.sqrt(variance)
