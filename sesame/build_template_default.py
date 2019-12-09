#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from conans.client.conan_api import Conan
from sesame import build_shared

import cpt.builds_generator

def get_builder(pure_c=False):

    builder = build_shared.get_builder()
    builder.add_common_builds(pure_c=pure_c)

    return builder
