# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import platform

import sesame
import bincrafters.build_shared

def build_cmd(args):
    """Build a recipe"""
    parser = argparse.ArgumentParser(description=build_cmd.__doc__, prog='sesame build')
    parser.add_argument('--upload', action='store_true', default=False)
    parser.add_argument("--user", '-u', help="Conan user that the package will be created under.", default='sesame')
    parser.add_argument("--channel", '-c', help="Conan channel that the package will be created under.", default='testing')

    parser.add_argument("--default-profile", help="Uses sesame-default.profile instead of i.e. sesame-base-windows.profile", default=False, action="store_true")
    parser.add_argument("--build-missing", help="Build missing deps", default=False, action="store_true")

    parser.add_argument("--android", help="builds for android", default=False, action="store_true")
    parser.add_argument("--emscripten", help="builds for emscripten", default=False, action="store_true")
    parser.add_argument("--linux", help="builds for linux", default=False, action="store_true")
    parser.add_argument("--macos", help="builds for macOS", default=False, action="store_true")
    parser.add_argument("--uwp", help="builds for UWP", default=False, action="store_true")
    parser.add_argument("--windows", help="builds for windows", default=False, action="store_true")

    args = parser.parse_args(*args)
    _build(args)

def _build(args):
    completed = subprocess.run(['conan', 'profile', 'list'], stdout=subprocess.PIPE, encoding='utf=8', check=True)
    if not 'sesame-default.profile' in completed.stdout:
        subprocess.run(['conan', 'profile', 'new', '--detect', 'sesame-default.profile'], check=True)
        subprocess.run(['conan', 'profile', 'update', 'settings.build_type=RelWithDebInfo', 'sesame-default.profile'], check=True)
        #for item in ['settings.os', 'settings.arch', 'settings.build_type', 'settings.compiler', 'settings.compiler.version', 'settings.compiler.libcxx']:
        #    subprocess.run(['conan', 'profile', 'remove', item, 'sesame-default.profile'], check=False)
    target_path = os.path.expanduser('~/.conan/settings.yml')
    if os.path.exists(target_path):
        os.remove(target_path)
    shutil.copy(sesame.get_conan_settings_yml_path(), target_path)

    common_conan_env = {
        'CONAN_USERNAME': f'{args.user}',
        'CONAN_CHANNEL': f'{args.channel}',
        'CONAN_VERSION': bincrafters.build_shared.get_version_from_recipe(),

        'CONAN_PIP_PACKAGE': 'False',
        'CONAN_BUILD_TYPES': 'Debug,RelWithDebInfo',

        'CONAN_UPLOAD': 'https://api.bintray.com/conan/orhun/sesame',
        'CONAN_STABLE_BRANCH_PATTERN': 'dontupload',
        'CONAN_UPLOAD_ONLY_WHEN_STABLE': '1',
    }

    upload_conan_env = {}
    if args.upload:
        upload_conan_env = {
            'CONAN_STABLE_BRANCH_PATTERN': 'master|sesame/master',
        }

    build_conan_env = {}
    if args.build_missing:
        build_conan_env = {
            'CONAN_BUILD_POLICY': 'missing'
        }

    for build in [['android', args.android],
                  ['emscripten', args.emscripten],
                  ['linux', args.linux],
                  ['macos', args.macos],
                  ['uwp', args.uwp],
                  ['windows', args.windows]]:
        name = build[0]
        active = build[1]
        if active:
            platform_conan_env = _prepare_conan_env(args, prep_for=name)
            conan_env = {**common_conan_env, **upload_conan_env, **build_conan_env, **platform_conan_env}

            build_script = 'build.py'
            if os.path.isfile('build-sesame.py'):
                build_script = 'build-sesame.py'
            subprocess.run(['python', build_script], check=True, cwd='.', env={**os.environ.copy(), **conan_env})

def _prepare_conan_env(args, prep_for):
    env = {}

    env['SESAME_BUILD_FOR'] = prep_for
    if args.default_profile:
        env['CONAN_BASE_PROFILE'] = 'sesame-default.profile'
    else:
        env['CONAN_BASE_PROFILE'] = sesame.get_conan_profiles_path(f'sesame-base-{prep_for}.profile')

    if prep_for == 'android':
        env['CONAN_CLANG_VERSIONS'] = '7.0'
        env['CONAN_ARCHS'] = 'armv8,x86'
    elif prep_for == 'emscripten':
        pass
    elif prep_for == 'linux':
        env['CONAN_CLANG_VERSIONS'] = '6.0'
        env['CONAN_ARCHS'] = 'x86_64'
    elif prep_for == 'macos':
        env['CONAN_APPLE_CLANG_VERSIONS'] = '9.1'
        env['CONAN_ARCHS'] = 'x86_64'
    elif prep_for == 'uwp':
        env['CONAN_VISUAL_VERSIONS'] = '15'
        env['CONAN_VISUAL_RUNTIMES'] = 'MD, MDd'
        env['CONAN_ARCHS'] = 'x86_64'
    elif prep_for == 'windows':
        env['CONAN_VISUAL_VERSIONS'] = '15'
        env['CONAN_VISUAL_RUNTIMES'] = 'MD, MDd'
        env['CONAN_ARCHS'] = 'x86_64'

    return env
