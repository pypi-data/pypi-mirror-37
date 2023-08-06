from gtable import Table
import numpy as np
from itertools import chain
from gtable.fast import join_low_level, reindex_join_columns, \
    intersection_sorted, union_sorted


def inner_join(table_left, table_right, column):
    """
    Inner join. If columns are repeated, the left table has preference.

    :param table_left:
    :param table_right:
    :param column:
    :return:
    """
    if column not in table_left.keys:
        raise ValueError('{} not in left table'.format(column))

    if column not in table_right.keys:
        raise ValueError('{} not in right table'.format(column))

    all_columns = set(chain(table_left.keys, table_right.keys))
    joined_columns = all_columns - {column}

    common_left = table_left.get(column)
    common_right = table_right.get(column)

    if not np.all(common_left.values == np.sort(common_left.values)):
        raise ValueError('Trying to join with a non sorted column')

    if not np.all(common_right.values == np.sort(common_right.values)):
        raise ValueError('Trying to join with a non sorted column')

    common_rec = intersection_sorted(common_left.values, common_right.values)

    data_joined, global_left, global_right = join_low_level(
        common_left.values, common_left.index,
        common_right.values, common_right.index, common_rec)

    data = list()
    index = list()
    keys = list()

    data.append(data_joined)
    index.append(np.ones(len(data_joined), dtype=np.uint8))
    keys.append(column)

    for i_column in joined_columns:
        if i_column in table_left:
            c = table_left.get(i_column)
            c = c.reindex(global_left)
            keys.append(i_column)
            data.append(c.values)
            index.append(c.index)

        elif i_column in table_right:
            c = table_right.get(i_column)
            c = c.reindex(global_right)
            keys.append(i_column)
            data.append(c.values)
            index.append(c.index)

    res = Table()
    res.data = data
    res.index = np.vstack(index)
    res.keys = keys

    return res


def full_outer_join(table_left, table_right, column, check_sorted=True):
    """
    Inner join. If columns are repeated, the left table has preference.

    :param table_left:
    :param table_right:
    :param column:
    :param check_sorted: If True may increase performance, but breaks if the
      column used as index is not sorted.
    :return:
    """
    if column not in table_left.keys:
        raise ValueError('{} not in left table'.format(column))

    if column not in table_right.keys:
        raise ValueError('{} not in right table'.format(column))

    all_columns = set(chain(table_left.keys, table_right.keys))
    joined_columns = all_columns - {column}

    common_left = table_left.get(column)
    common_right = table_right.get(column)

    if check_sorted:
        if not np.all(common_left.values == np.sort(common_left.values)):
            raise ValueError('Trying to join with a non sorted column')

        if not np.all(common_right.values == np.sort(common_right.values)):
            raise ValueError('Trying to join with a non sorted column')

    common_rec = union_sorted(common_left.values, common_right.values)

    data_joined, global_left, global_right = join_low_level(
        common_left.values, common_left.index,
        common_right.values, common_right.index, common_rec)

    data = list()
    index = list()
    keys = list()

    data.append(data_joined)
    index.append(np.ones(len(data_joined), dtype=np.uint8))
    keys.append(column)

    for i_column in joined_columns:
        if (i_column in table_left) and (i_column in table_right):
            cl = table_left.get(i_column)
            cr = table_right.get(i_column)
            c_values, c_index = reindex_join_columns(
                cl, cr, global_left, global_right)
            keys.append(i_column)
            data.append(c_values)
            index.append(c_index)

        elif i_column in table_left:
            c = table_left.get(i_column)
            c = c.reindex(global_left)
            keys.append(i_column)
            data.append(c.values)
            index.append(c.index)

        elif i_column in table_right:
            c = table_right.get(i_column)
            c = c.reindex(global_right)
            keys.append(i_column)
            data.append(c.values)
            index.append(c.index)

    res = Table()
    res.data = data
    res.index = np.vstack(index)
    res.keys = keys

    return res

