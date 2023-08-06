#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.3.2'

from .producer import FlavorApkProducer
import checker


def fromFile(filePath):
    return FlavorApkProducer().fromFile(filePath)


def reportApkFilesInfo(destFiles):
    checker.reportApkFilesInfo(destFiles)
