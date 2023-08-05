#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkg_resources

def score_dir():
  d = pkg_resources.resource_filename(__name__, 'scores')
  print('Scores are located at `%s\'' % d)
