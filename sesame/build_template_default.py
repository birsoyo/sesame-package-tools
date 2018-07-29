#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sesame.build_shared
import bincrafters.build_shared


def get_builder(shared_option_name=None,
                pure_c=True,
                dll_with_static_runtime=False,
                build_policy=None):

    builder = sesame.build_shared.get_builder(build_policy)
    if shared_option_name is None and sesame.build_shared.is_shared():
        shared_option_name = "%s:shared" % bincrafters.build_shared.get_name_from_recipe()

    builder.add_common_builds(
        shared_option_name=shared_option_name,
        pure_c=pure_c,
        dll_with_static_runtime=dll_with_static_runtime)

    return builder
