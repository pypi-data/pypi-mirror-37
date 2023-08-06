#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Iterable as _Iterable

from .providers import PROVIDERS, _Provider


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
