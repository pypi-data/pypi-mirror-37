# `ilinkedlist`

This module is an implementation of immutable linked lists. A linked list is
defined as either `nil` or a `Pair` whose `cdr` is a linked list. Linked lists
are hashable. Note that it is possible to create an improper list by passing a
non-list as the second argument to `Pair`. Almost all functions in this module
ignore the last `cdr` of a list and assume that it's `nil`.

Linked lists are useful, because they can be built element-by-element in O(n).
Tuples require O(n^2) due to having to copy the tuple with each new element.
Traditional Python lists require O(n*log(n)), because some new elements will
trigger a memory reallocation (and therefore a copy).

## `nil`

A singleton value representing the empty linked list. It essentially behaves
like an empty sequence.

## `def isList(x)`

Return `True` if `x` is either `nil` or a `Pair`, otherwise `False`.

## `def new(iterable)`

Return a new linked list with the elements from `iterable`.

## `def reverse(iterable)`

Return a new linked list with the elements from `iterable` in reverse order.
This function is faster than `new` if you don't want to preserve order.

## class `Pair(car, cdr)`

This class is used as the linked list node. `cdr` is the item to be stored in
this node. `cdr` is usually a linked list. Passing a non-linked list as `cdr`
will result in an improper list. The terminology is inspired by LISP.

`nil` and `Pair` objects both define the same methods, listed below.

## `ll[i]`

Return element `i` from the list. If `i` is a slice, return the desired elements
in a linked list.

## `a == b`
## `a != b`
## `a < b`
## `a <= b`
## `a > b`
## `a >= b`

Linked lists follow the normal rules for sequence comparison.

## `llA + llB`

Concatenate two linked lists.

## `iterable + ll`

Concatenate the elements of `iterable` to the beginning of `ll`.

## `ll * n`

Concatenate `ll` to itself `n` times.

## `hash(ll)`

Linked lists are hashable.

## `iter(ll)`

Yield each element in `ll`.

## `repr(ll)`

`repr(ilinkedlist.nil)` simply returns `'nil'`. The `repr` of a Pair is a `new`
invocation with a tuple argument.

## `reversed(ll)`

Return a new linked list with the elements of `ll` in reverse order.

## `str(ll)`

`str(ilinkedlist.nil)` simply returns `'nil'`. The `str` of a Pair is a
space-separated list of elements in parentheses.

## `ll.appendReverse(iterable)`

Append the elements of `iterable`, in reverse order, to the beginning of `ll`.
Return the resulting list. This is the most basic function we use for iterative
list construction. It is generally faster than other functions that return
lists, including `__add__`, which must call this function twice.

## `ll.count(x)`

Return the number of times `x` is in `ll`.

## `ll.delItem(index)`

Return a copy of `ll` with the item at `index` deleted. `index` may be a
`slice`.

## `ll.headReverse(n)`

Return a linked list of the first `n` items in reverse order.

## `ll.insert(index, x)`

Return a copy of `ll` with `x` inserted after `index` nodes.

## `ll.member(x)`

Return the first sublist whose `car` equals `x`. If `x` is not in the list,
return `None` (not `nil`). We provide this method instead of the `index` method
of sequences, because for linked lists, it's more natural to refer to an item's
position by node than by index.

## `ll.nodes()`

Return an iterator that yields each `Pair` in `ll`. The `StopIteration` value is
the last `cdr`, which is usually `nil`.

## `ll.pop([i])`

Return a 2-element tuple containing, respectively, the element at index `i` and
a copy of `ll` with that element removed. The default value of `i` is `0`,
unlike the default argument of `list.pop`.

## `ll.remove(x)`

Return a copy of `ll` with the first item equal to `x` removed.

## `ll.setItem(index, value)`

Return a copy of the `ll` with the item at `index` changed to `value`. `index`
may be a `slice`, in which case `value` must be iterable.

## `ll.sort(key=None, reverse=None)`

Return a sorted version of `ll`. The keyword arguments are the same as with the
`sorted` builtin.

## `ll.splitAtFast(index)`

Equivalent to `(ll.headReverse(index), ll.tail(index))`, but faster.

## `ll.tail(index)`

Return the sublist starting after the first `index` nodes. If index is greater
than the length of the list, return `nil`. Equivalent to `ll[index:]`.
