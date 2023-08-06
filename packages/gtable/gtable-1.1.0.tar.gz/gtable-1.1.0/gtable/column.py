import numpy as np
import operator
from gtable.lib import fillna_column
from gtable.fast import apply_fast_add, apply_fast_mul, apply_fast_truediv, \
    apply_fast_sub, apply_fast_floordiv, apply_fast_and, apply_fast_or, \
    apply_fast_xor, apply_fast_pow, apply_fast_mod, apply_fast_ge, \
    apply_fast_gt, apply_fast_le, apply_fast_lt, apply_fast_eq, apply_fast_ne, \
    apply_mask_column, reindex_column


class Column:
    """
    Indexed column view of the table
    """
    def __init__(self, values, index):
        self.values = values
        self.index = index

    def __repr__(self):
        return "<Column[ {} ] object at {}>".format(self.values.dtype,
                                                    hex(id(self)))

    def __add__(self, y):
        return apply_add(self, y)

    def __radd__(self, y):
        return apply_add(self, y)

    def __sub__(self, y):
        return apply_truediv(self, y)

    def __rsub__(self, y):
        return apply_truediv(self, y)

    def __mul__(self, y):
        return apply_mul(self, y)

    def __rmul__(self, y):
        return apply_mul(self, y)

    def __truediv__(self, y):
        return apply_truediv(self, y)

    def __rtruediv__(self, y):
        return apply_truediv(self, y)
    
    def __floordiv__(self, y):
        return apply_floordiv(self, y)

    def __rfloordiv__(self, y):
        return apply_floordiv(self, y)

    def __pow__(self, y):
        return apply_pow(self, y)

    def __mod__(self, y):
        return apply_mod(self, y)

    def __lt__(self, y):
        return apply_lt(self, y)

    def __le__(self, y):
        return apply_le(self, y)

    def __gt__(self, y):
        return apply_gt(self, y)

    def __ge__(self, y):
        return apply_ge(self, y)

    def __eq__(self, y):
        return apply_eq(self, y)

    def __ne__(self, y):
        return apply_ne(self, y)

    def __and__(self, y):
        return apply_and(self, y)

    def __or__(self, y):
        return apply_or(self, y)

    def __xor__(self, y):
        return apply_xor(self, y)

    def __neg__(self):
        return Column(-self.values, self.index)

    def __getitem__(self, i):
        # TODO: This algorithm makes getitem O(N)
        if self.index[i]:
            return self.values[int(self.index[:i+1].sum()) - 1]
        else:
            return None

    def __len__(self):
        return len(self.index)

    def copy(self):
        """Return a copy of the column"""
        return Column(self.values[:], self.index[:])

    def astype(self, dtype):
        """Changes the (numpy) datatype of the values"""
        self.values[:] = self.values.astype(dtype)

    @property
    def dtype(self):
        """Returns the datatype of the column"""
        return self.values.dtype

    def fillna(self, reverse=False, fillvalue=None):
        """
        Fills the non available value sequentially with the previous
        available position. Operates inplace.
        """
        self.values, self.index = fillna_column(self.values, self.index,
                                                reverse, fillvalue)

    def fill(self, fillvalue):
        """
        Fills the N/A values of the column with the fillvalue
        :param fillvalue:
        :return:
        """
        new_values = np.empty(len(self.index), dtype=self.values.dtype)
        bool_index = self.index.astype(np.bool_)

        if np.any(bool_index):
            new_values[bool_index] = self.values

        new_values[~bool_index] = fillvalue

        self.values = new_values
        self.index = np.ones(len(self.index))

    def reorder(self, order):
        """
        Reorder the column inplace
        :param order:
        :return:
        """
        self.values[:] = self.values[(np.cumsum(self.index) - np.array(1)
                                      )[order[self.index.astype(np.bool)]]]
        self.index[:] = self.index[order]

    def mask(self, mask):
        """
        Apply mask on data to the data and the index out of place
        :param mask:
        :return:
        """
        return Column(*apply_mask_column(self.values, self.index, mask))

    def reindex(self, index):
        """
        Reindex according to a global index

        :param index:
        :return:
        """
        return Column(*reindex_column(self.values, self.index, index))

    def date_range(self, fr='1970-01-01', to='2262-01-01', include_fr=True,
                   include_to=True):
        """
        Filter a column by date range.

        :param fr:
        :param to:
        :param include_fr:
        :param include_to:
        :return:
        """
        if isinstance(self.values.dtype, np.datetime64):
            print(self.values.dtype)
            raise ValueError("Method valid only with dates")

        if type(fr) == str:
            fr = np.datetime64(fr)

        if type(to) == str:
            to = np.datetime64(to)

        if include_fr:
            before = self.values >= fr
        else:
            before = self.values > fr

        if include_to:
            after = self.values <= to
        else:
            after = self.values < to

        return Column(before & after, self.index)

    def is_empty(self):
        """
        True if the column is empty

        :return:
        """
        return self.values.shape == (0,)

    def is_sorted(self):
        """
        True if the column is sorted
        :return:
        """
        return np.sort(self.values) == self.values

    def contains(self, item):
        """
        Returns a column with the value of the column present in item.

        :param item:
        :return:
        """
        if isinstance(item, np.ndarray):
            return Column(np.in1d(self.values, item), self.index)
        elif type(item) == Column:
            return Column(np.in1d(self.values, item.values), self.index)
        else:
            raise ValueError('Argument must be an array or a column.')


def apply_add(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_add(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)
    else:
        return Column(operator.add(left.values, right), left.index)


def apply_sub(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_sub(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.sub(left.values, right), left.index)

    
def apply_mul(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_mul(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.mul(left.values, right), left.index)


def apply_truediv(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_truediv(left.values, right.values,
                                           left.index, right.index)
        return Column(result, index)
        
    else:
        return Column(operator.truediv(left.values, right), left.index)
    
    
def apply_floordiv(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_floordiv(left.values, right.values,
                                            left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.floordiv(left.values, right), left.index)


def apply_pow(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_pow(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.pow(left.values, right), left.index)


def apply_mod(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_mod(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.mod(left.values, right), left.index)
    

def apply_gt(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_gt(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.gt(left.values, right), left.index)


def apply_ge(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_ge(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.ge(left.values, right), left.index)

    
def apply_lt(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_lt(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.lt(left.values, right), left.index)

    
def apply_le(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_le(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.le(left.values, right), left.index)

    
def apply_and(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_and(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.and_(left.values.astype(np.bool), right),
                      left.index)

    
def apply_or(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_or(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.or_(left.values.astype(np.bool), right),
                      left.index)
    

def apply_xor(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_xor(left.values, right.values,
                                       left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.xor(left.values.astype(np.bool), right),
                      left.index)

    
def apply_eq(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_eq(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.eq(left.values, right), left.index)

    
def apply_ne(left: Column, right):
    if type(right) == Column:
        result, index = apply_fast_ne(left.values, right.values,
                                      left.index, right.index)
        return Column(result, index)

    else:
        return Column(operator.ne(left.values, right), left.index)
