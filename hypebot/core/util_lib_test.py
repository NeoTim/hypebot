# Copyright 2018 The Hypebot Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for util_lib."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import arrow
import mock

from hypebot.core import util_lib


class UtilLibTest(unittest.TestCase):

  def testUnformatHypecoins(self):
    self.assertEqual(420, util_lib.UnformatHypecoins('420'))
    self.assertEqual(1234, util_lib.UnformatHypecoins('1.234k'))
    self.assertEqual(1000000, util_lib.UnformatHypecoins('1M'))
    self.assertEqual(2500000, util_lib.UnformatHypecoins('2.5M'))

  def testArrowTime(self):
    midnight_in_utc = util_lib.ArrowTime()
    raw_arrow_time = arrow.utcnow().replace(hour=0, minute=0, second=0,
                                            microsecond=0)
    self.assertEqual(raw_arrow_time, midnight_in_utc)

    est = 'US/Eastern'
    noon_in_est = util_lib.ArrowTime(12, 0, 0, est)
    raw_arrow_time = arrow.now(est).replace(hour=12, minute=0, second=0,
                                            microsecond=0)
    self.assertEqual(raw_arrow_time, noon_in_est)

    afternoon_in_local = util_lib.ArrowTime(16, tz='local')
    raw_arrow_time = arrow.now().replace(hour=16, minute=0, second=0,
                                         microsecond=0)
    self.assertEqual(raw_arrow_time, afternoon_in_local)

    morning_in_local = util_lib.ArrowTime(8, tz='local')
    morning_tomorrow = arrow.now().shift(days=1)
    morning_tomorrow = morning_tomorrow.replace(hour=8, minute=0, second=0,
                                                microsecond=0)
    self.assertNotEqual(morning_tomorrow, morning_in_local)

  @mock.patch('random.random')
  def testGetWeightedChoice(self, random_call):
    random_call.return_value = 0.25
    memes = ['ayyy', 'lmao', 'rito pls', 'who needs a test?']
    prob_table = []

    meme = util_lib.GetWeightedChoice(memes, prob_table)

    expected = [0.3125, 0.0625, 0.3125, 0.3125]

    self.assertEqual(expected, prob_table)
    self.assertEqual('lmao', meme)

    meme = util_lib.GetWeightedChoice(memes, prob_table)

    expected = [0.078125, 0.140625, 0.390625, 0.390625]

    self.assertEqual(expected, prob_table)
    self.assertEqual('ayyy', meme)

  def testFuzzyBool(self):
    for truthy_value in ('True', ' true', '1', 'ok', 'any_thing  ', 1, True):
      self.assertTrue(util_lib.FuzzyBool(truthy_value))

    for falsey_value in ('', '  falSe', '0', 'NO  ', 0, False):
      self.assertFalse(util_lib.FuzzyBool(falsey_value))

  def testExtractRegex_ReturnsNoneWhenNoMatch(self):
    self.assertIsNone(util_lib.ExtractRegex(r'.+', ''))

  def testExtractRegex_MultipleMatchesAreExtracted(self):
    # pytype can't seem to figure out that result isn't None (or isn't None
    # after asserting it isn't anyways). So we just use it directly instead of
    # destructuring the tuple.
    result = util_lib.ExtractRegex(r'[a-z]+', 'mone1234mtwo')
    self.assertIsNotNone(result)
    self.assertEqual(2, len(result[0]))
    self.assertIn('mone', result[0])
    self.assertIn('mtwo', result[0])
    self.assertEqual('1234', result[1])

  def testExtractRegex_NestedCapturesStillRemoveFullRegex(self):
    result = util_lib.ExtractRegex(r'g(.+)', 'Captures with groups')
    self.assertIsNotNone(result)
    self.assertEqual(1, len(result[0]))
    self.assertEqual('roups', result[0][0])
    self.assertEqual('Captures with ', result[1])


if __name__ == '__main__':
  unittest.main()
