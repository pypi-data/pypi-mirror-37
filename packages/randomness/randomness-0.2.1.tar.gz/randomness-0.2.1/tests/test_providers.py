#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from operator import attrgetter

from tests._context import randomness


def test_providers_not_empty():
    assert len(randomness.PROVIDERS) > 0


def test_providers_sorted():
    assert randomness.PROVIDERS == sorted(randomness.PROVIDERS, reverse=True)


@pytest.fixture(params=randomness.PROVIDERS, ids=attrgetter('name'))
def randomness_source(request):
    return request.param.cls()


def test_all_bits_take_both_states(randomness_source):

    """Verify that there are no stuck bits.

    The probability that this test nevertheless fails for a working and
    uniformly distributed randomness source is:

                                           n
                        ⎛         1      ⎞
        p       =   1 - ⎜ 1 - ―――――――――― ⎟      n = number of bits per run
         FAIL           ⎜       (r - 1)  ⎟      r = number of runs
                        ⎝      2         ⎠

    Except for very small r we can approximate this to:

                                  n
        p            ≅        ――――――――――
         FAIL                   (r - 1)
                               2

    Hence we do the following number of runs to keep the probability of
    a spurious failure below about one in a trillion:

        r   =   41 + ⌈ log₂ n ⌉

    """

    num_bits = 32
    all_bits_set = (1 << num_bits) - 1

    result_or = 0
    result_and = all_bits_set

    for _ in range(41 + (num_bits - 1).bit_length()):

        bits = randomness_source.getrandbits(num_bits)
        assert bits & all_bits_set == bits

        result_or |= bits
        result_and &= bits

    assert result_and == 0
    assert result_or == all_bits_set
