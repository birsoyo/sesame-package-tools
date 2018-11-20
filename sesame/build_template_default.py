#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from conans.client.conan_api import Conan
from sesame import build_shared

import cpt.builds_generator

def get_builder(shared_option_name=None,
                pure_c=True,
                dll_with_static_runtime=False,
                build_policy=None):

    builder = build_shared.get_builder(build_policy)

    if shared_option_name is None:
        conan_api, _, _ = Conan.factory(False)
        _, conanfile = conan_api.info('.')

        if 'shared' in conanfile.options:
            shared_option_name = f'{conanfile.name}:shared'

    # os_build = {
    #     'Windows': 'Windows',
    #     'Darwin': 'Macos',
    #     'Linux': 'Linux'
    # }.get(platform.system())

    # common_settings = {
    #     'os_build': os_build,
    #     'arch_build': 'x86_64'
    # }

    # prep_for = os.environ['SESAME_BUILD_FOR']
    # build_types = os.environ['SESAME_BUILD_TYPES'].split(',')
    # archs = os.environ['SESAME_ARCHS'].split(',')

    # print(f'{prep_for}:{build_types}:{archs}')

    builder.add_common_builds(
        shared_option_name=shared_option_name,
        pure_c=pure_c,
        dll_with_static_runtime=dll_with_static_runtime)
    return builder
