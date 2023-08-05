#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = ['get_center']

def get_center(end, start=1.):
  # We need this function to remind us the fact that:
  #   the center of a segment depends on both the start and the end position.
  # instead of simply using center = end / 2.
  return (end - start) / 2.