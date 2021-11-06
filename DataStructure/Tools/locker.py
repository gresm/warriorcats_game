"""
Why did I do this file?
"""
from __future__ import annotations
from typing import Callable, overload


class LockingError(Exception):
    pass


class _Locker:
    def __init__(self, func: Callable, allow_multiple_unlocking: bool = False):
        self.unlocked = False
        self.func = func
        self.allow_multiple_unlocking = allow_multiple_unlocking
        self.parent = None

    def __call__(self, *args, **kwargs):
        if self.unlocked and not self.allow_multiple_unlocking:
            raise LockingError("already unlocked")
        self.unlocked = True

        if self.parent:
            return self.func(self.parent, *args, **kwargs)
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        self.parent = instance
        return self

    @property
    def locked(self):
        return _LockedNotSetup(self)


class _LockedNotSetup:
    def __init__(self, locker: _Locker):
        self.locker = locker

    def __call__(self, func: Callable):
        return _Locked(self.locker, func)


class _Locked:
    def __init__(self, locker: _Locker, func: Callable):
        self.locker = locker
        self.func = func
        self.parent = None
        self.bait_func = _LockedFunction(func)

    def __get__(self, instance, owner):
        self.parent = instance
        if not instance:
            return self

        if self.locker.unlocked:
            return self.func
        else:
            return self.bait_func

    def __call__(self, *args, **kwargs):
        if self.locker.unlocked:
            if self.parent:
                return self.func(self.parent, *args, **kwargs)
            return self.func(*args, **kwargs)
        raise LockingError("function locked")


class _LockedFunction:
    def __init__(self, connected_to):
        self.connected_to = connected_to

    def __call__(self, *args, **kwargs):
        raise LockingError("function locked")

    def __repr__(self):
        return f"<Locked Function of ({repr(self.connected_to)})>"


@overload
def lock(allow_multiple_unlocking: bool) -> Callable[[Callable], _Locker]:
    pass


@overload
def lock(func: Callable) -> _Locker:
    pass


def lock(*args, **kwargs):
    names = ["func", "allow_multiple_unlocking"]
    optionals = {"allow_multiple_unlocking": True}
    fixed = {}

    if len(args) > len(names):
        raise KeyError("too many arguments")

    for el in range(len(args)):
        fixed[names[el]] = args[el]

    fixed.update(kwargs)
    opt_copy = optionals.copy()
    opt_copy.update(fixed)
    fixed = opt_copy

    if set(fixed) != set(names):
        raise KeyError(f"expected {len(names)} arguments, got: {len(fixed)}")

    return _lock(**fixed)


def _lock(func: Callable, allow_multiple_unlocking: bool):
    return _Locker(func, allow_multiple_unlocking)
