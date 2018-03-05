###
# Copyright (c) 2018, Anatoly Popov
# Copyright (c) 2018, Andrey Rahmatullin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import random
import pytest
from .sevenSea2EdRaiseRoller import Raise, RollResult, SevenSea2EdRaiseRoller

class TestAssembler:
    def test_zero_dice(self):
        x = SevenSea2EdRaiseRoller(lambda x: range(1, x+1)).roll_and_count(0)
        assert len(x.raises) == 0
        assert len(x.unused) == 0
        assert str(x) == "0 raises"

    def test_zero_raises_one_dice(self):
        x = SevenSea2EdRaiseRoller(lambda x: range(1, x+1)).roll_and_count(1)
        assert len(x.raises) == 0
        assert len(x.unused) == 1
        assert str(x) == "0 raises, unused: 1"

    def test_green(self):
        x = SevenSea2EdRaiseRoller(lambda x: range(1, x+1)).roll_and_count(4)
        assert len(x.raises) == 1
        assert len(x.unused) == 0
        assert str(x) == "1 raise: *(4 + 3 + 2 + 1)"

    def test_explode(self):
        rolls = SevenSea2EdRaiseRoller(ExplodingRoller().roll).roll(1)
        assert rolls == [10]

        rolls = SevenSea2EdRaiseRoller(ExplodingRoller().roll, explode=True).roll(1)
        assert rolls == [10, 5]

        rolls = SevenSea2EdRaiseRoller(ExplodingRoller(3).roll, explode=True).roll(1)
        assert rolls == [10, 10, 10, 5]

        rolls = SevenSea2EdRaiseRoller(ExplodingRoller(3).roll, explode=True).roll(3)
        assert rolls == [10, 10, 10, 5, 10, 10, 10, 5, 10, 10, 10, 5]

    def test_big_skill(self):
        rolls = SevenSea2EdRaiseRoller(
            lambda x: [8, 6, 1, 8, 5, 2, 4],
            skill_rank=7
        ).roll_and_count(7)
        assert str(rolls) == "4 raises: **(8 + 6 + 1), **(8 + 5 + 2), unused: 4"

class Roller:
    def roll(self, count):
        return [next(self) for _ in range(count)]

class ExplodingRoller(Roller):
    def __init__(self, ten_count=1, default_value=5):
        self.ten_count = ten_count
        self.current_ten_count = ten_count
        self.default_value = default_value

    def __next__(self):
        if self.current_ten_count == 0:
            self.current_ten_count = self.ten_count
            return self.default_value
        else:
            self.current_ten_count -= 1
            return 10
