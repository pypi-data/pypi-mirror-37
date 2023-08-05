#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

__all__ = ['Tee']

class Tee(object):
  """
  From: http://web.archive.org/web/20141016185743/https://mail.python.org/pipermail/python-list/2007-May/460639.html
  Usage:
    tee=Tee('logfile', 'w')
    print 'abcdefg'
    print 'another line'
    tee.close()
    print 'screen only'
    del tee # should do nothing
  """
  def __init__(self, name, mode):
    self.file = open(name, mode)
    self.stdout = sys.stdout
    sys.stdout = self
  def close(self):
    if self.stdout is not None:
      sys.stdout = self.stdout
      self.stdout = None
    if self.file is not None:
      self.file.close()
      self.file = None
  def write(self, data):
    self.file.write(data)
    self.stdout.write(data)
  def flush(self):
    self.file.flush()
    self.stdout.flush()
  def __del__(self):
    self.close()