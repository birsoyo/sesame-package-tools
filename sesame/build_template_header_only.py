#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sesame import build_shared

def get_builder():
    builder = build_shared.get_builder()
    builder.add()
    return builder
