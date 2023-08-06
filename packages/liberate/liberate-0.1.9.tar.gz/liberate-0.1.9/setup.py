#!/usr/bin/env python3
# -*- coding: utf8 -*-

from setuptools import setup

setup(
  name='liberate',
  version='0.1.9',
  description='Video/Audio/Url liberation (to .ogg)',
  author='Nichlas Severinsen',
  author_email='ns@nsz.no',
  url='https://notabug.org/necklace/liberate',
  packages=['liberate'],
  scripts=['liberate/liberate'],
  install_requires=["youtube_dl", "colorama"]
)
