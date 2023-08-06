#!/usr/bin/python3

"""A module to manage configuring a project."""

import os.path
import os

import devpipeline_core.config.parser
import devpipeline_configure.cache
import devpipeline_configure.version


def split_list(values, split_string=","):
    """
    Convert a delimited string to a list.

    Arguments
    values -- a string to split
    split_string -- the token to use for splitting values
    """
    return [value.strip() for value in values.split(split_string)]


def _is_cache_dir_appropriate(cache_dir, cache_file):
    """
    Determine if a directory is acceptable for building.

    A directory is suitable if any of the following are true:
      - it doesn't exist
      - it is empty
      - it contains an existing build cache
    """
    if os.path.exists(cache_dir):
        files = os.listdir(cache_dir)
        if cache_file in files:
            return True
        return not bool(files)
    return True


def _add_default_options(config, state):
    for key, value in state.items():
        config["DEFAULT"][key] = value


def _make_src_dir(config, package_name):
    src_path = None
    if "src_path" in config:
        src_path = config.get("src_path")
        if os.path.isabs(src_path):
            return src_path
    if not src_path:
        src_path = package_name
    return os.path.join(config.get("dp.src_root"), src_path)


_PACKAGE_OPTIONS = {
    "dp.build_dir": lambda config, package_name: os.path.join(
        config.get("dp.build_root"), package_name),
    "dp.src_dir": _make_src_dir
}


def _add_package_options(config, package_name, state):
    # pylint: disable=unused-argument
    for key, option_fn in _PACKAGE_OPTIONS.items():
        config[key] = option_fn(config, package_name)


def _add_package_options_all(config, state):
    for package in config.sections():
        _add_package_options(config[package], package, state)


def _create_cache(raw_path, cache_dir, cache_file):
    if _is_cache_dir_appropriate(cache_dir, cache_file):
        config = devpipeline_core.config.parser.read_config(raw_path)
        abs_path = os.path.abspath(raw_path)
        root_state = {
            "dp.build_config": abs_path,
            "dp.src_root": os.path.dirname(abs_path),
            "dp.version": format(devpipeline_configure.version.ID, "02x")
        }
        root_state["dp.build_root"] = os.path.join(os.getcwd(), cache_dir)
        _add_default_options(config, root_state)
        _add_package_options_all(config, root_state)
        return config
    raise Exception(
        "{} doesn't look like a dev-pipeline folder".format(cache_dir))


def _write_config(config, cache_dir, cache_file):
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    with open(os.path.join(cache_dir, cache_file), 'w') as output_file:
        config.write(output_file)


def _set_list(config, kwargs_key, config_key, **kwargs):
    values = kwargs.get(kwargs_key)
    if values:
        config["DEFAULT"][config_key] = values


_CONFIG_MODIFIERS = [
    lambda config, **kwargs: _set_list(config, "profiles",
                                       "dp.profile_name", **kwargs),
    lambda config, **kwargs: _set_list(config, "overrides",
                                       "dp.overrides", **kwargs)
]


def process_config(raw_path, cache_dir, cache_file, **kwargs):
    """
    Read a build configuration and create it, storing the result in a build
    cache.

    Arguments
    raw_path -- path to a build configuration
    cache_dir -- the directory where cache should be written
    cache_file -- The filename to write the cache.  This will live inside
                  cache_dir.
    **kwargs -- additional arguments used by some modifiers
    """
    config = _create_cache(raw_path, cache_dir, cache_file)
    for modifier in _CONFIG_MODIFIERS:
        modifier(config, **kwargs)
    _write_config(config, cache_dir, cache_file)
    # pylint: disable=protected-access
    return devpipeline_configure.cache._CachedConfig(
        config, os.path.join(cache_dir, cache_file))
