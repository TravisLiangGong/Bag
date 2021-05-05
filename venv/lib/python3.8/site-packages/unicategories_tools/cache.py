"""unicategories cache module."""

import io
import os
import os.path
import pickle
import unicodedata
import warnings

import unicategories_tools as tools

try:
    from importlib.resources import open_binary as open_binary_resource
except ImportError:
    from pkg_resources import resource_stream as open_binary_resource

try:
    import typing as t
except ImportError:
    pass

cache_formats = ('0.0.6', 'v1')
cache_version = unicodedata.unidata_version


def load_from_package(package, resource):
    # type: (str, str) -> t.Optional[t.Dict[str, tools.RangeGroup]]
    """
    Try to load category ranges from module.

    :returns: category ranges dict or None
    """
    try:
        with open_binary_resource(package, resource) as f:
            version, fmt, data = pickle.load(f)
        if version == cache_version and fmt in cache_formats:
            return data
        warnings.warn((
            'Unicode unicategories database is outdated. '
            'Please reinstall unicategories module to regenerate it.'
            if version < cache_version else
            'Incompatible unicategories database. '
            'Please reinstall unicategories module to regenerate it.'
            ))
    except (ValueError, EOFError):
        warnings.warn((
            'Incompatible unicategories database. '
            'Please reinstall unicategories module to regenerate it.'
            ))
    except IOError:
        pass
    return None


def load_from_cache(path=None):
    # type: (t.Optional[str]) -> t.Optional[t.Dict[str, tools.RangeGroup]]
    """
    Try to load category ranges from userlevel cache file.

    :param path: path to userlevel cache file
    :returns: category ranges dict or None
    """
    if not path:
        return None
    try:
        with io.open(path, 'rb') as f:
            version, fmt, data = pickle.load(f)
        if version == cache_version and fmt in cache_formats:
            return data
    except (IOError, ValueError, EOFError):
        pass
    return None


def generate_and_cache(path=None):
    # type: (t.Optional[str]) -> t.Dict[str, tools.RangeGroup]
    """
    Generate category ranges and save to userlevel cache file.

    :param path: path to userlevel cache file
    :returns: category ranges dict
    """
    data = tools.generate()  # type: t.Dict[str, tools.RangeGroup]
    if not path:
        return data
    try:
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with io.open(path, 'wb') as f:
            pickle.dump((cache_version, cache_formats[-1], data), f)
    except (IOError, ValueError) as e:
        warnings.warn('Unable to write cache file %r: %r' % (path, e))
    return data
