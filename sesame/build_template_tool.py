#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from sesame import build_shared

def get_builder(**kwargs):
    builder = build_shared.get_builder(**kwargs)

    os_build = {
        'Windows': 'Windows',
        'Darwin': 'Macos',
        'Linux': 'Linux'}.get(platform.system())
    builder.add(settings={'os_build': os_build, 'arch_build': 'x86_64'})
    return builder
