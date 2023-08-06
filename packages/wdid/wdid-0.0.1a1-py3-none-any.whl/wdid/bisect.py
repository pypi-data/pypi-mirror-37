import typing as typ
from logging import Logger
from typing import Generic, TypeVar

T = typ.TypeVar("T")


def bisect_matches_range(
    array: typ.Sequence[T], cmp: typ.Callable[[T], typ.Optional[int]]
) -> typ.Tuple[int, int]:
    start = bisect_matches_left(array, cmp)
    return start, bisect_matches_right(array, cmp, lo=start)


def bisect_matches_get_range(
    array: typ.Sequence[T], cmp: typ.Callable[[T], typ.Optional[int]]
) -> typ.Sequence[T]:
    start, end = bisect_matches_range(array, cmp)
    return array[start:end]


def bisect_matches_right(
    array: typ.Sequence[T],
    cmp: typ.Callable[[T], typ.Optional[int]],
    lo: int = 0,
    hi: typ.Optional[int] = None,
) -> int:
    """Return the index where to insert item x in list a, assuming a is sorted.
    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        high = len(array)
    else:
        high = hi
    low, high = min((lo, high), (high, lo))
    low = min(max(0, low), len(array))
    high = min(max(0, high), len(array))
    del lo, hi
    while low < high:
        mid = (low + high) // 2
        cmp_res = cmp(array[mid])
        if cmp_res is None:
            low_test = bisect_matches_right(array, cmp, lo=low, hi=mid - 1)
            if low_test == mid - 1:
                return bisect_matches_right(array, cmp, lo=mid + 1, hi=high)
            else:
                return low_test
        elif cmp_res < 0:
            high = mid
        else:
            low = mid + 1
    return low


def bisect_matches_left(
    array: typ.Sequence[T],
    cmp: typ.Callable[[T], typ.Optional[int]],
    lo: int = 0,
    hi: typ.Optional[int] = None,
) -> int:
    """Return the index where to insert item x in list a, assuming a is sorted.
    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if hi is None:
        high = len(array)
    else:
        high = hi
    low, high = min((lo, high), (high, lo))
    low = min(max(0, low), len(array))
    high = min(max(0, high), len(array))
    del lo, hi
    while low < high:
        mid = (low + high) // 2
        cmp_res = cmp(array[mid])
        if cmp_res is None:
            low_test = bisect_matches_left(array, cmp, lo=mid + 1, hi=high)
            if low_test == mid + 1:
                return bisect_matches_left(array, cmp, lo=low, hi=mid - 1)
            else:
                return low_test
        elif cmp_res < 0:
            low = mid + 1
        else:
            high = mid
    return low
