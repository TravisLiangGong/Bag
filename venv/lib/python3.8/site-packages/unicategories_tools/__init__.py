"""unicategories tools module."""

import bisect
import collections
import itertools
import sys
import unicodedata

try:
    import typing as t
    T = t.TypeVar('T')
except ImportError:
    pass

if sys.version_info < (3, ):
    chr = unichr  # noqa
    range = xrange  # noqa
    map = itertools.imap  # noqa


class RangeGroup(tuple):
    """
    Immutable iterable representing a list of unicode code point ranges.

    Every range is reperesented using a tuple (start, end), with **end** itself
    being outside range for compatibility with python's :func:`range` builtin.

    It is assumed given data does not contain any overlapping range and it is
    already sorted from small to bigger range start. If it is not, use
    :func:`unicategories.merge` to fix values prior to passing to this.
    """

    def __new__(cls, range_list=()):
        # type: (t.Type[RangeGroup], t.Tuple[t.Iterable[int]]) -> RangeGroup
        """
        Create and return a new object.

        See help(type) for accurate signature.
        """
        return super(RangeGroup, cls).__new__(cls, map(tuple, range_list))

    def __add__(self, other):
        # type: (RangeGroup, RangeGroup) -> RangeGroup
        """
        Return self+value.

        x.__add__(y) <==> x+y
        """
        return merge(self, other)

    def __mul__(self, mult):
        # type: (RangeGroup, int) -> RangeGroup
        """
        Return self*value.

        x.__mul__(n) <==> x*n
        """
        return self

    def characters(self):
        # type: (RangeGroup) -> t.Iterator[t.Text]
        """
        Get iterator with all characters on this range group.

        :returns: iterator of characters (unicode/str of size 1)
        """
        return map(chr, self.codes())

    def codes(self):
        # type: (RangeGroup) -> t.Iterator[int]
        """
        Get iterator for all unicode code points contained in this range group.

        :returns: iterator of character indexes (int)
        """
        for start, end in self:
            for item in range(start, end):
                yield item

    def has(self, character):
        # type: (RangeGroup, t.Union[t.Text, str, int]) -> bool
        """
        Get if character (or character code point) is part of this range group.

        :param character: character or unicode code point to look for
        :returns: True if character is contained by any range, False otherwise
        """
        if not self:
            return False
        character = character if isinstance(character, int) else ord(character)
        last = self[-1][-1]
        start, end = self[bisect.bisect_right(self, (character, last)) - 1]
        return start <= character < end

    def __repr__(self):
        # type: (RangeGroup) -> str
        """
        Return repr(self).

        repr(object) -> string

        Return the canonical string representation of the object.
        For most object types, eval(repr(object)) == object.
        """
        return '%s(%s)' % (
            self.__class__.__name__,
            super(RangeGroup, self).__repr__(),
            )


def merge(*range_lists, **kwargs):
    # type: (...) -> RangeGroup
    """
    Merge one or multiple range groups into a single one, without overlap.

    No typechecking is performed, so a valid range group will be any iterable
    (or iterator) containing an (start, end) iterable pair. Result type will
    be defined by group_class parameter (defaults to RangeGroup).

    :param range_lists: several range groups to join
    :param group_class: result type, defaults to RangeGroup
    :returns: merged range group
    """
    group_class = kwargs.pop('group_class', RangeGroup)
    range_list = [
        unirange
        for range_list in range_lists
        for unirange in range_list
        ]
    range_list.sort()
    it = iter(range_list)
    slast, elast = last = list(next(it))
    result = [last]
    for start, end in it:
        if start > elast:
            slast, elast = last = [start, end]
            result.append(last)
        elif end > elast:
            last[1] = elast = end
    return group_class(result)


def generate(categorize=unicodedata.category, group_class=RangeGroup):
    # type: (t.Callable[[t.Text], str], t.Type[T]) -> t.Dict[str, T]
    """
    Generate dict of unicode categories and their RangeGroups.

    RangeGroups corresponding to general unicode categories are also included.

    :param categorize: category function, defaults to unicodedata.category.
    :param group_class: class for range groups, defaults to RangeGroup
    :returns: dictionary of categories and range groups
    """
    categories = collections.defaultdict(list)
    last_category = None
    last_range = [None, None]
    for c in range(sys.maxunicode + 1):
        category = categorize(chr(c))
        if category != last_category:
            last_category = category
            last_range[1] = c
            last_range = [c, None]
            categories[last_category].append(last_range)
    last_range[1] = c + 1
    categories = {k: group_class(v) for k, v in categories.items()}
    categories.update({
        k: merge(*map(categories.__getitem__, g))
        for k, g in itertools.groupby(sorted(categories), key=lambda k: k[0])
        })
    return categories
