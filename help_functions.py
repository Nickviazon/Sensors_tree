def indexes(itr, element, comparison='eq'):
    """
    Returns list of indexes all elements of an iterable object,
    which correspond to the comparison with the element of 'parameter'
    :param itr - the iterable object where you want to find the indexes of 'element'
    :param element - the element with which you want to compare
    :param comparison - comparison operation

    There is 6 provided comparison operations:
      'eq' - equal;
      'not_eq' - not equal;
      'grt' - strictly greater than;
      'lss' - strictly less than;
      'lss_eq' - less than or equal;
      'grt_eq' - greater than or equal.

    Example:

      a = [1, 2, 10, 23, 45]
      indexes(a, 10, 'lss') # Will return [0,1]
    """
    if comparison == 'eq':
        return [i for i, elem in enumerate(itr) if element == elem]
    elif comparison == 'not_eq':
        return [i for i, elem in enumerate(itr) if element != elem]
    elif comparison == 'grt':
        return [i for i, elem in enumerate(itr) if element < elem]
    elif comparison == 'lss':
        return [i for i, elem in enumerate(itr) if element > elem]
    elif comparison == 'grt_eq':
        return [i for i, elem in enumerate(itr) if element <= elem]
    elif comparison == 'lss_eq':
        return [i for i, elem in enumerate(itr) if element >= elem]
