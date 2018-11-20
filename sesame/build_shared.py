#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cpt.packager import ConanMultiPackager
from cpt.builds_generator import BuildGenerator, get_mingw_builds, get_visual_builds, get_linux_clang_builds, get_linux_gcc_builds, get_osx_apple_clang_builds

def _get_builds(self, pure_c, shared_option_name, dll_with_static_runtime, reference=None):
    ref = reference or self._reference

    if self._os_name == "Windows":
        if self._mingw_configurations:
            builds = get_mingw_builds(self._mingw_configurations,
                                        get_mingw_package_reference(), self._archs,
                                        shared_option_name, self._build_types, self._options, ref)
        else:
            builds = []
        builds.extend(get_visual_builds(self._visual_versions, self._archs,
                                        self._visual_runtimes, self._visual_toolsets,
                                        shared_option_name, dll_with_static_runtime,
                                        self._vs10_x86_64_enabled,
                                        self._build_types, self._options, ref))
        return builds
    elif self._os_name == "Linux":
        builds = get_linux_gcc_builds(self._gcc_versions, self._archs, shared_option_name,
                                        pure_c, self._build_types, self._options, ref)
        builds.extend(get_linux_clang_builds(self._clang_versions, self._archs,
                                                shared_option_name, pure_c, self._build_types,
                                                self._options, ref))
        return builds
    elif self._os_name == "Darwin":
        return get_osx_apple_clang_builds(self._apple_clang_versions, self._archs,
                                            shared_option_name, pure_c, self._build_types, self._options, ref)
    elif self._os_name == "FreeBSD":
        return get_linux_clang_builds(self._clang_versions, self._archs, shared_option_name,
                                        pure_c, self._build_types, self._options, ref)
    elif self._os_name == "Android":
        return get_linux_clang_builds(self._clang_versions, self._archs, shared_option_name,
                                        pure_c, self._build_types, self._options, ref)
    elif self._os_name == "Emscripten":
        return get_linux_clang_builds(self._clang_versions, self._archs, shared_option_name,
                                        pure_c, self._build_types, self._options, ref)
    else:
        raise Exception("Unknown operating system: %s" % self._os_name)


def get_builder(build_policy=None):
    BuildGenerator.get_builds = _get_builds

    platform_info = None
    build_for = os.getenv('SESAME_BUILD_FOR', '')
    if build_for == 'android':
        class AndroidPlatformInfo(object):
            @staticmethod
            def system():
                return 'Android'
        platform_info = AndroidPlatformInfo()
    elif build_for == 'emscripten':
        class EmscriptenPlatformInfo(object):
            @staticmethod
            def system():
                return 'Emscripten'
        platform_info = EmscriptenPlatformInfo()

    builder = ConanMultiPackager(platform_info=platform_info)
    return builder

    """
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
"""