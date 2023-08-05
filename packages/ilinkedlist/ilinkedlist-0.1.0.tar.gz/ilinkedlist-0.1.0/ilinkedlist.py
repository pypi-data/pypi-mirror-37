# Copyright 2018 Luther Thompson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License (GPL3) as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You have the following additional permission: You may convey the program in
# object code form under the terms of sections 4 and 5 of GPL3 without being
# bound by section 6 of GPL3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""An immutable linked list library.

A linked list is defined as either nil or a Pair whose cdr is a linked list.
Linked lists are hashable. Note that it is possible to create an improper list
by passing a non-list as the second argument to Pair. Almost all functions in
this module ignore the last cdr of a list and assume that it's nil.

Linked lists are useful, because they can be built element-by-element in O(n).
Tuples require O(n^2) due to having to copy the tuple with each new element.
Traditional Python lists require O(n*log(n)), because some new elements will
trigger a memory reallocation (and therefore a copy).
"""

# Import each thing as a single, non-colliding name.
from abc import abstractmethod
import collections.abc as abc
import itertools
import operator

__all__ = 'nil', 'Pair', 'new', 'reverse', 'isList'


def _normalizeIndex(size, i):
  """Convert i to a non-negative index."""
  return i + (size if i < 0 else 0)


def _compareLists(a, b, compare):
  """Compare two lists using compare to compare each item.

  If one list is a prefix of the other, compare lengths instead.
  """
  for x, y in zip(a, b):
    if x != y:
      return compare(x, y)
  return compare(len(a), len(b))


class _List(abc.Hashable, abc.Reversible, abc.Sized):
  """The abstract base class for nil and Pair."""

  __slots__ = ()

  @abstractmethod
  def __repr__(self):
    pass

  def nodes(self):
    """Return an iterator that yields each Pair in the linked list.

    The StopIteration value is the last cdr, which is usually nil.
    """
    while _isPair(self):
      yield self
      self = self.cdr
    return self

  def __iter__(self):
    for node in self.nodes():
      yield node.car

  def __eq__(self, other):
    return _compareLists(self, other, operator.eq)

  def __lt__(self, other):
    return _compareLists(self, other, operator.lt)

  def __le__(self, other):
    return _compareLists(self, other, operator.le)

  def __gt__(self, other):
    return _compareLists(self, other, operator.gt)

  def __ge__(self, other):
    return _compareLists(self, other, operator.ge)

  def __reversed__(self):
    return reverse(self)

  def tail(self, index):
    """Return the list starting after the first index nodes.

    If i is greater than the length of the list, return nil. Equivalent to
    self[i:].
    """
    for i, node in enumerate(self.nodes()):
      if i >= index:
        return node
    return nil

  def __getitem__(self, key):
    """Get the key-th element of the list."""
    size = len(self)
    if isinstance(key, int):
      i = _normalizeIndex(size, key)
      error = IndexError(f'Index out of range: {key}')
      if i < 0:
        raise error
      for x in self:
        if not i:
          return x
        i -= 1
      raise error
    if isinstance(key, slice):
      s = key.indices(size)
      return (
        self.tail(s[0])
        if s[1] >= size and s[2] == 1
        else new(itertools.islice(self, key.start, key.stop, key.step))
      )
    raise TypeError(f'Index must be int or slice, got {key}')

  def appendReverse(self, head):
    """Append the elements of head, in reverse order, to the beginning of self.

    Return the resulting list. Faster than concatenation.
    """
    for x in head:
      self = Pair(x, self)
    return self

  def __add__(self, other):
    """Concatenate two linked lists."""
    return other.appendReverse(reverse(self))

  def __radd__(self, other):
    """Concatenate a non-linked list to a linked list. Return a linked list."""
    return self.appendReverse(reverse(other))

  def __mul__(self, n):
    if n <= 0:
      return nil
    lst = self
    for i in range(n - 1):
      lst = self + lst
    return lst

  def __rmul__(self, n):
    return self * n

  def member(self, x):
    """Return the first sublist whose car equals x.

    If x is not in the list, return None (not nil). We provide this method
    instead of the index method of sequences, because for linked lists, it's
    more natural to refer to an item's position by node than by index.
    """
    for node in self.nodes():
      if node.car == x:
        return node

  def count(self, x):
    """Return the number of times x is in the list."""
    c = 0
    for item in self:
      if item == x:
        c += 1
    return c

  def headReverse(self, index):
    """Return a list of the first index items in reverse order.

    Faster than a slice.
    """
    lst = nil
    for x in itertools.islice(self, index):
      lst = Pair(x, lst)
    return lst

  def splitAt(self, index):
    """Return a tuple containing the head and tail of the list, split at index.

    The head is in reverse order.
    """
    head = nil
    for i, node in enumerate(self.nodes()):
      if i >= index:
        return head, node
      head = Pair(node.car, head)
    return head, nil

  def setItem(self, key, value):
    """Return a copy of the list with the item at key changed to value.

    key may be a slice object, in which case value must be iterable.
    """
    if isinstance(key, int):
      i = _normalizeIndex(len(self), key)
      head, main = self.splitAt(i)
      return Pair(value, main.tail(1)).appendReverse(head)
    if isinstance(key, slice):
      start = key.start or 0
      size = key.stop - start
      head, main = self.splitAt(start)
      tail = main.tail(size)
      if key.step is None:
        return (value + tail).appendReverse(head)
      valueIter = iter(value)
      iRange = range(0, size, key.step)
      return (
        (
          next(valueIter) if i in iRange else x
          for i, x in itertools.islice(enumerate(main), size)
        ) + tail
      ).appendReverse(head)
    raise TypeError(f'Index must be int or slice, got {key}')

  def delItem(self, key):
    """Return a copy of the list without the indicated values."""
    if isinstance(key, int):
      i = _normalizeIndex(len(self), key)
      head, main = self.splitAt(i)
      return main.tail(1).appendReverse(head)
    if isinstance(key, slice):
      start = key.start or 0
      size = key.stop - start
      head, main = self.splitAt(start)
      tail = main.tail(size)
      if key.step is None:
        return tail.appendReverse(head)
      iRange = range(0, size, key.step)
      return (
        (
          x
          for i, x in itertools.islice(enumerate(main), size)
          if i not in iRange
        ) + tail
      ).appendReverse(head)
    raise TypeError(f'Index must be int or slice, got {key}')

  def insert(self, i, x):
    """Return a copy of the list with x inserted after i nodes."""
    head, tail = self.splitAt(i)
    return Pair(x, tail).appendReverse(head)

  def remove(self, x):
    """Return a copy of the list without the first instance of x."""
    head = nil
    for node in self.nodes():
      if node.car == x:
        return node.cdr.appendReverse(head)
      head = Pair(node.car, head)
    raise ValueError(f'{x} not in {self}')

  def sort(self, key=None, reverse=False):
    """Return a sorted version of the list."""
    # We can't use appendReverse here, because that would make the sort
    # unstable.
    return new(sorted(self, key=key, reverse=reverse))

  def pop(self, i=0):
    """Return element i and the list without that element.

    Return a 2-element tuple containing, respectively, the element at index `i`
    and a copy of `ll` with that element removed. The default value of `i` is
    `0`, unlike the default argument of `list.pop`.
    """
    head, tail = self.splitAt(i)
    return tail.car, tail.cdr.appendReverse(head)


def isList(x):
  """Return True if x is nil or a Pair, otherwise False."""
  return isinstance(x, _List)


class _NilType(_List):
  """The singleton class for nil."""

  __slots__ = ()

  def __len__(self):
    return 0

  def __hash__(self):
    return 0

  def __repr__(self):
    return 'nil'


def _isNil(x):
  return x is nil


class Pair(_List):
  """The linked list node."""

  __slots__ = 'car', 'cdr', '_len'

  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr
    self._len = (len(cdr) if _isPair(cdr) else 0) + 1

  def __len__(self):
    """Return the length of the list."""
    return self._len

  def __hash__(self):
    return hash((self.car, self.cdr))

  def __repr__(self):
    lst = ' '.join(repr(x) + ',' for x in self)
    return f'new(({lst}))'

  def __str__(self):
    lst = ' '.join(str(x) for x in self)
    return f'({lst})'


def _isPair(x):
  return isinstance(x, Pair)


def reverse(iterable):
  """Reverse iterable and turn it into a linked list.

  This function is faster than new if you don't want to preserve order.
  """
  return nil.appendReverse(iterable)


def new(iterable):
  """Build a linked list from iterable."""
  return reverse(reverse(iterable))


# The empty linked list.
nil = _NilType()
