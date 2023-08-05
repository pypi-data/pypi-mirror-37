#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

__all__ = ['sort_nicely',
           'list_diff',
           'evenly_sample']


def tryfloat(s):
  try:
    return float(s)
  except:
    return s


def alphanum_key(s):
  """ Turn a string into a list of string and number chunks.
      "z23a" -> ["z", 23, "a"]
  """
  return [tryfloat(c) for c in re.split('([0-9.]+)', s)]


def sort_nicely(l):
  """ Sort the given list in the way that humans expect.
  """
  return sorted(l, key=alphanum_key)

def list_diff(a, b, order_matter=True):
  if order_matter:
    diff = [item for item in a if item not in set(b)]
  else:
    diff = list(set(a) - set(b))
  return diff

evenly_sample = lambda m, n: [i * m // n + m // (2 * n) for i in range(n)]
