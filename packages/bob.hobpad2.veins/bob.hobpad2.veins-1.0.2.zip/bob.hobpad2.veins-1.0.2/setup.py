#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from setuptools import setup, dist
dist.Distribution(dict(setup_requires = ['bob.extension']))

from bob.extension.utils import load_requirements, find_packages
install_requires = load_requirements()

setup(

    name = 'bob.hobpad2.veins',
    version = open("version.txt").read().rstrip(),
    description = 'Software package to reproduce experiments of Chapter 18, "An Introduction to Vein Presentation Attacks and Detection" of the "Handbook of Biometric Anti-Spoofing: Presentation Attack Detection 2nd Edition" book',

    url = 'https://gitlab.idiap.ch/bob/bob.hobpad2.veins',
    license = 'GPLv3',
    author = 'Andre Anjos',
    author_email = 'andre.anjos@idiap.ch',
    keywords = 'bob',
    long_description = open('README.rst').read(),
    packages = find_packages('bob'),
    include_package_data = True,
    install_requires = install_requires,
    entry_points = {
      'console_scripts': [
        'bob_hobpad2_veins_scores.py = bob.hobpad2.veins.script:score_dir',
        ],
      'bob.bio.config': [
        'mc_bio = bob.hobpad2.veins.configurations.mc_bio',
        'mc_pa = bob.hobpad2.veins.configurations.mc_pa',
        'rlt_bio = bob.hobpad2.veins.configurations.rlt_bio',
        'rlt_pa = bob.hobpad2.veins.configurations.rlt_pa',
        'wld_bio = bob.hobpad2.veins.configurations.wld_bio',
        'wld_pa = bob.hobpad2.veins.configurations.wld_pa',
        ],
      },
    classifiers = [
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
