#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Wed 14 Mar 22:08:06 2018 CET

"""This configuration runs the following experiment:

- same configuration as mc_bio
- use matching attacks instead of bona fide probes
- runs fast
"""

from .mc_bio import *
protocol += '-va'
