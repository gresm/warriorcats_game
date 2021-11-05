"""
Why did I do this file?
"""
from typing import Callable, overload


class LockingError(Exception):
    pass


class _Locker:
    def __init__(self, func: Callable[[...], ...], allow_multiple_unlocking: bool = False):
        self.unlocked = False
        self.func = func
        self.allow_multiple_unlocking = allow_multiple_unlocking

    @property
    def locked(self):
        return _LockedNotSetup(self)

    def __call__(self, *args, **kwargs):
        if self.unlocked and not self.allow_multiple_unlocking:
            raise LockingError("already unlocked")
        self.unlocked = True
        return self.func(*args, **kwargs)


class _LockedNotSetup:
    def __init__(self, locker: _Locker):
        self.locker = locker

    def __call__(self, func: Callable[[...], ...]):
        return _Locked(self.locker, func)


class _Locked:
    def __init__(self, locker: _Locker, func: Callable[[...], ...]):
        self.locker = locker
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.locker.unlocked:
            return self.func(*args, **kwargs)
        raise LockingError("function locked")


@overload
def lock(allow_multiple_unlocking: bool) -> Callable[[Callable[[...], ...]], _Locker]:
    pass


@overload
def lock(func: Callable[[...], ...]) -> _Locker:
    pass


def lock(*args, **kwargs):
    names = ["func", "allow_multiple_unlocking"]
    optionals = {"allow_multiple_unlocking": False}
    fixed = {}

    if len(args) > len(names):
        raise KeyError("too many arguments")

    for el in range(len(args)):
        fixed[names[el]] = args[el]

    fixed.update(kwargs)
    opt_copy = optionals.copy()
    opt_copy.update(fixed)
    fixed = opt_copy

    if len(fixed) != len(names):
        raise KeyError(f"expected {len(names)} arguments, got: {len(fixed)}")
