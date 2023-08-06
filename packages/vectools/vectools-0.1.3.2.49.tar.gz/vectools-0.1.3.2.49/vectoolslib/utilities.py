"""
This method contains various functions that are widely used in other methods.
"""


def convert_to_positive_index(negative_index, iter_len):
    """

    :param negative_index:
    :param iter_len:
    :return:
    """
    return negative_index if negative_index >= 0 else iter_len + negative_index


def pythonic_coordinates_to_exact_coordinates_list(slice_str, iter_len, split_char=",", slice_char=":"):
    """

    :param slice_str:
    :param iter_len:
    :param split_char:
    :param slice_char:
    :return:
    """
    assert type(iter_len) == int
    coordinate_list = []
    for token in slice_str.split(split_char):

        if slice_char in token:
            # e.g., a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]; a[2:5] = [2, 3, 4]
            start, stop = token.split(slice_char)

            # Check for negative indexes
            # a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]; a[-2] = 8
            # len(a) = 10; 10 - 2 = 8
            start = convert_to_positive_index(int(start), iter_len)
            stop = convert_to_positive_index(int(stop), iter_len)

            # Check for things that will mess up the range.

            if stop > start:
                coordinate_list += [i for i in range(start, stop)]
            elif stop < start:
                # We don't care about order since we are returning a set
                start, stop = stop, start
                coordinate_list += reversed([i for i in range(start, stop)])
            else:  # stop == start:
                print("ERROR: '%s' start and stop columns match." % token)
                exit()

        else:
            coordinate = convert_to_positive_index(int(token), iter_len)
            coordinate_list.append(coordinate)

    return coordinate_list
