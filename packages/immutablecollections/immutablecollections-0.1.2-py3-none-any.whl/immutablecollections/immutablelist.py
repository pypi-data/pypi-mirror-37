from abc import ABCMeta
from typing import Generic, Iterable, Iterator, List, Sequence, Sized, Tuple, TypeVar

from attr import attrib, attrs

from immutablecollections.immutablecollection import ImmutableCollection

T = TypeVar('T')  # pylint:disable=invalid-name
T2 = TypeVar('T2')


class ImmutableList(Generic[T], ImmutableCollection[T], Sequence[T], Iterable[T],
                    metaclass=ABCMeta):
    __slots__ = ()

    # Signature of the of method varies by collection
    # pylint: disable = arguments-differ
    @staticmethod
    def of(seq: Iterable[T]) -> 'ImmutableList[T]':
        if isinstance(seq, ImmutableList):
            return seq
        else:
            return ImmutableList.builder().add_all(seq).build()  # type: ignore

    @staticmethod
    def empty() -> 'ImmutableList[T]':
        return EMPTY_IMMUTABLE_LIST

    @staticmethod
    def builder() -> 'ImmutableList.Builder[T]':
        return ImmutableList.Builder()

    class Builder(Generic[T2], Sized):
        def __init__(self):
            self._list: List[T2] = []

        def add(self, item: T2) -> 'ImmutableList.Builder[T2]':
            self._list.append(item)
            return self

        def add_all(self, items: Iterable[T2]) -> 'ImmutableList.Builder[T2]':
            self._list.extend(items)
            return self

        def __len__(self) -> int:
            return len(self._list)

        def build(self) -> 'ImmutableList[T2]':
            if self._list:
                return _TupleBackedImmutableList(self._list)
            else:
                return EMPTY_IMMUTABLE_LIST

    def __repr__(self):
        return 'i' + str(self)

    def __str__(self):
        return "%s" % list(self)


@attrs(frozen=True, slots=True, repr=False)
class _TupleBackedImmutableList(ImmutableList[T]):

    _list: Tuple[T, ...] = attrib(converter=tuple)

    def __getitem__(self, index: int) -> T:
        return self._list.__getitem__(index)

    def __iter__(self) -> Iterator[T]:
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()


# Singleton instance for empty
EMPTY_IMMUTABLE_LIST: ImmutableList = _TupleBackedImmutableList(())
