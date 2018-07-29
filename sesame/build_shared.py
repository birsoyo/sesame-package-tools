#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cpt.packager import ConanMultiPackager
from cpt.packager import PlatformInfo

import bincrafters.build_shared
import os

def is_shared():
    match = bincrafters.build_shared.get_value_from_recipe(r'''options = ([\s\S]*?)(?=}|$)''')
    if match is None:
        return False
    return "shared" in match.groups()[0]

def get_builder(build_policy=None):
    name = bincrafters.build_shared.get_name_from_recipe()
    username, channel, version, login_username = bincrafters.build_shared.get_conan_vars()
    reference = "{0}/{1}".format(name, version)
    upload = bincrafters.build_shared.get_conan_upload(username)
    remotes = os.getenv("CONAN_REMOTES", bincrafters.build_shared.get_conan_remotes(username))
    upload_when_stable = bincrafters.build_shared.get_upload_when_stable()
    stable_branch_pattern = os.getenv("CONAN_STABLE_BRANCH_PATTERN", "stable/*")
    archs = bincrafters.build_shared.get_archs()
    build_policy = os.getenv('CONAN_BUILD_POLICY', build_policy)

    platform_info = None
    build_for = os.getenv('SESAME_BUILD_FOR', '')
    if build_for == 'android':
        class AndroidPlatformInfo(object):
            @staticmethod
            def system():
                return 'Android'
        platform_info = AndroidPlatformInfo()

    builder = ConanMultiPackager(
        username=username,
        login_username=login_username,
        channel=channel,
        reference=reference,
        upload=None,
        remotes=remotes,
        archs=archs,
        build_policy=build_policy,
        upload_only_when_stable=upload_when_stable,
        stable_branch_pattern=stable_branch_pattern,
        platform_info=platform_info)

    return builder
