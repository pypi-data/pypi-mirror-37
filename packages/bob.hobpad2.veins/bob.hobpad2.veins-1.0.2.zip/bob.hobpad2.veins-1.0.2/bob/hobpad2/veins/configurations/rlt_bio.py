#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Wed 14 Mar 22:08:06 2018 CET

"""This configuration runs the following experiment:

- verafinger database, verification using protocol Nom
- preprocessing using annotations
- feature extraction using repeated line tracking with default parameters
- miura matching
- features go to "./results/features/rlt"
- scores go to "./results/scores/rlt/Nom/nonorm"
- on my MacBook Air from 2012, it takes about 2 hours to run this experiment
"""

from bob.bio.vein.configurations.verafinger import *
protocol = 'Nom'

from bob.bio.vein.configurations.repeated_line_tracking import *

from bob.bio.vein.preprocessor import NoCrop, AnnotatedRoIMask, \
  HuangNormalization, NoFilter, Preprocessor

preprocessor = Preprocessor(
    crop=NoCrop(),
    mask=AnnotatedRoIMask(),
    normalize=HuangNormalization(),
    filter=NoFilter(),
    )
"""Preprocessing using RoI annotations
"""

temp_directory = 'results/features'
result_directory = 'results/scores'
"""Directory where results are stored"""

sub_directory = 'rlt'
"""Sub-directory where results should be stored"""

verbose = 2
"""Make the application slightly verbose"""
