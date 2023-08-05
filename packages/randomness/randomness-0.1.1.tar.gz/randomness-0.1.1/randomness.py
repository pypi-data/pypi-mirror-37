#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Any as _Any,
    Iterable as _Iterable,
    List as _List,
)

import enum as _enum
import os as _os
import random as _random

from collections import namedtuple as _namedtuple

__all__ = [
    'ProviderFlag',
    'PROVIDERS',
    'get_range',
]


class ProviderFlag(_enum.Flag):
    FULLY_DETERMINISTIC = PSEUDORANDOM = PSEUDO_RANDOM = PRNG = _enum.auto()
    NONDETERMINISTIC = NON_DETERMINISTIC = TRULY_RANDOM = TRNG = _enum.auto()
    NEVER_BLOCKING = NONBLOCKING = NON_BLOCKING = _enum.auto()
    CLONEABLE = FORKABLE = RESTORABLE = SNAPSHOTTABLE = STATEFUL = _enum.auto()
    SEEDABLE = _enum.auto()
    FAST = QUICK = _enum.auto()
    CRYPTOGRAPHICALLY_SECURE = _enum.auto()
    CRYPTOGRAPHICALLY_STRONG = _enum.auto()
    PROTECTED_MEMORY = _enum.auto()
    THREADSAFE = _enum.auto()


_Provider = _namedtuple('Provider', ['precedence', 'name', 'cls', 'flags'])

PROVIDERS = [
    _Provider(
            precedence=-11,
            name='mersenne_twister',
            cls=_random.Random,
            flags=(
                    ProviderFlag.FULLY_DETERMINISTIC |
                    ProviderFlag.NEVER_BLOCKING |
                    ProviderFlag.CLONEABLE |
                    ProviderFlag.SEEDABLE |
                    ProviderFlag.FAST
            ),
    ),
    _Provider(
            precedence=9,
            name='system',
            cls=_random.SystemRandom,
            flags=ProviderFlag(0),
    ),
]

try:
    # noinspection PyStatementEffect
    _os.getrandom

except AttributeError:
    pass

else:
    class URandom(_random.Random):

        _GETRANDOM_FLAGS = 0

        def __init__(self, x=None) -> None:
            super().__init__(x)
            self._entropy = 0
            self._entropy_bits = 0

        def random(self) -> float:
            return self.getrandbits(_random.BPF) * _random.RECIP_BPF

        def getrandbits(self, k: int) -> int:
            assert k > 0

            missing_bytes = (k - self._entropy_bits + 7) // 8
            while missing_bytes > 0:
                random_bytes = _os.getrandom(missing_bytes,
                                             flags=self._GETRANDOM_FLAGS)
                random_bytes_count = len(random_bytes)
                self._entropy |= (int.from_bytes(random_bytes, 'little') <<
                                  self._entropy_bits)
                self._entropy_bits += random_bytes_count * 8
                missing_bytes -= random_bytes_count

            result = self._entropy & ((1 << k) - 1)
            self._entropy >>= k
            self._entropy_bits -= k
            return result

        # noinspection PyMethodOverriding
        def _randbelow(self, n: int) -> int:
            assert n > 0

            if n == 1:
                return 0

            k = (n - 1).bit_length()
            r = self.getrandbits(k)
            while r >= n:
                r = self.getrandbits(k)

            return r

        def seed(self, *args, **kwargs) -> None:
            pass

        def getstate(self) -> _Any:
            raise NotImplementedError

        def setstate(self, state: _Any) -> None:
            raise NotImplementedError

    PROVIDERS += [
        _Provider(
                precedence=49,
                name='urandom',
                cls=URandom,
                flags=(
                        ProviderFlag.CRYPTOGRAPHICALLY_SECURE
                ),
        ),
    ]

    try:
        # noinspection PyStatementEffect
        _os.GRND_RANDOM

    except AttributeError:
        pass

    else:
        # noinspection PyAbstractClass
        class Random(URandom):

            _GETRANDOM_FLAGS = _os.GRND_RANDOM

        PROVIDERS += [
            _Provider(
                    precedence=99,
                    name='random',
                    cls=Random,
                    flags=(
                            ProviderFlag.NONDETERMINISTIC |
                            ProviderFlag.CRYPTOGRAPHICALLY_SECURE |
                            ProviderFlag.CRYPTOGRAPHICALLY_STRONG
                    ),
            ),
        ]


try:
    import rdrand as _rdrand

except ImportError:
    _rdrand = None

else:
    if _rdrand.HAS_RAND:
        PROVIDERS += [_Provider(
                precedence=19,
                name='rdrand',
                cls=_rdrand.RdRandom,
                flags=(
                        ProviderFlag.NEVER_BLOCKING |
                        ProviderFlag.FAST |
                        ProviderFlag.CRYPTOGRAPHICALLY_SECURE
                ),
        )]

    if _rdrand.HAS_SEED:
        PROVIDERS += [_Provider(
                precedence=69,
                name='rdseed',
                cls=_rdrand.RdSeedom,
                flags=(
                        ProviderFlag.NONDETERMINISTIC |
                        ProviderFlag.NEVER_BLOCKING |
                        ProviderFlag.CRYPTOGRAPHICALLY_SECURE |
                        ProviderFlag.CRYPTOGRAPHICALLY_STRONG
                ),
        )]


def get_range(context: _random.Random, low: int, high: int, k: int,
              inverted=False) -> _List:
    population = range(low, high + 1)

    if inverted:
        k = len(population) - k

    sample = context.sample(population, k)

    if not inverted:
        return sample

    remainder = set(population)
    remainder.difference_update(sample)
    return sorted(remainder)


PROVIDERS.sort(reverse=True)


if __name__ == '__main__':
    def _test(providers: _Iterable[_Provider]) -> None:
        import sys

        for provider in providers:
            print(f"\n{provider.name}:\n", file=sys.stderr, flush=True)

            random = provider.cls()

            for expression in [
                'random.getrandbits(4096).bit_length()',
                'random.random()',
                'random.randint(-11, -10)',
                'random.randrange(16)',
            ]:
                print(f"{expression} = {eval(expression)!r}",
                      file=sys.stderr, flush=True)

    _test(PROVIDERS)
