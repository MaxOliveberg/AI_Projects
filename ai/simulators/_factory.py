from typing import Generic, TypeVar


T = TypeVar("T")


class Factory(Generic[T]):
    """Factories are callable objects that spawn simulator instances."""

    __pdoc__ = {
        "Factory.__call__": True
    }

    def __init__(self, cls: T, *args, **kwargs):
        """
        Args:
            cls (T): Simulator class.
            `*args, **kwargs`: arguments and key-word arguments passed to the simulator
                `__init__` method.
        """
        super().__init__()
        self._cls = cls
        self._args = args
        self._kwargs = kwargs

    def __call__(self) -> T:
        return self._cls(*self._args, **self._kwargs)
