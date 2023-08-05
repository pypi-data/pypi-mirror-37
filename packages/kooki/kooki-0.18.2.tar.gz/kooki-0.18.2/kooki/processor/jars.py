import os, glob, yaml

from functools import lru_cache

from packaging import version
from kooki.config import get_kooki_dir_jars, get_kooki_jar_config
from kooki.tools import read_config_file

from .exception import TooMuchResult, KookiJarOutdated
from ..version import __version__


def check_kooki_jar_version(jar_name):
    jar_config = get_kooki_jar_config(jar_name)
    if jar_config and 'kooki' in jar_config:
        minimum_kooki_version_needed = jar_config['kooki']
        if version.parse(__version__) < version.parse(minimum_kooki_version_needed):
            raise KookiJarOutdated(jar_name, __version__, minimum_kooki_version_needed)


def jar_dependencies(jar_name):
    jar_config = get_kooki_jar_config(jar_name)
    if jar_config and 'dependencies' in jar_config:
        return jar_config['dependencies']
    else:
        return []


def search_jar(jar):
    if '==' in jar:
        jar = jar.split('==')[0]
    ret_jar_path = None
    user_jars_dir = get_kooki_dir_jars()
    jar_path = os.path.join(user_jars_dir, jar)
    if os.path.isdir(jar_path):
        ret_jar_path = jar_path
    return ret_jar_path


def get_search_paths(jars):
    directories = []
    directories.append(os.getcwd())
    directories += get_jars_path(jars)
    return directories


def get_jars_path(jars):
    user_jars_dir = get_kooki_dir_jars()
    directories = []
    for jar in jars:
        if '==' in jar:
            jar = jar.split('==')[0]
        jar_path = os.path.join(user_jars_dir, jar)
        resource_jar_path = os.path.join(jar_path)
        directories.append(resource_jar_path)
    return directories

@lru_cache(maxsize=256)
def search_file_in_context(document, extension_path, path):
    context = os.path.join(os.getcwd(), document.context)
    directory_path = os.path.dirname(extension_path)
    search_path = os.path.join(os.path.join(directory_path, path))
    if search_path.startswith(context):
        return search_file_in_path(search_path)
    else:
        return None

@lru_cache(maxsize=256)
def search_file(document, filename):
    ret_file_path = None
    ret_file_path = search_file_in_local(os.path.join(document.context, filename))
    jars = list(reversed(document.jars))
    if not ret_file_path:
        ret_file_path = search_file_in_jars(jars, filename)        
    return ret_file_path


def search_file_in_local(filename):
    ret_file_path = None
    file_path = os.path.join(os.getcwd(), filename)
    ret_file_path = search_file_in_path(file_path)
    return ret_file_path


def search_file_in_jars(jars, filename):
    user_jars_dir = get_kooki_dir_jars()
    ret_file_path = None
    for jar in jars:
        if '==' in jar:
            jar = jar.split('==')[0]
        jar_path = os.path.join(user_jars_dir, jar)
        ret_file_path = search_file_in_jar(jar_path, filename)
        if ret_file_path:
            break
    return ret_file_path


def search_file_in_jar(jar_path, filename):
    ret_file_path = None
    file_path = os.path.join(jar_path, filename)
    ret_file_path = search_file_in_path(file_path)
    return ret_file_path


def search_file_in_path(file_path):
    if os.path.isdir(file_path):
        return file_path
    else:
        root, ext = os.path.splitext(file_path)
        result = glob.glob('{}.*'.format(file_path))

        if ext == '':
            result = glob.glob('{}.*'.format(file_path))
            if len(result) == 1:
                return result[0]
            elif len(result) > 1:
                raise TooMuchResult(file_path, result)
            return None
        else:
            if os.path.isfile(file_path):
                return file_path
            else:
                return None
