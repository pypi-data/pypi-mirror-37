#!/usr/bin/python3
"""This modules aggregates the available builders that can be used."""

import os.path
import os

import devpipeline_core.toolsupport

import devpipeline_build


def _nothing_builder(current_config):
    # Unused variables
    del current_config

    class _NothingBuilder:
        def configure(self, src_dir, build_dir):
            # pylint: disable=missing-docstring
            pass

        def build(self, build_dir):
            # pylint: disable=missing-docstring
            pass

        def install(self, build_dir, path):
            # pylint: disable=missing-docstring
            pass

    return _NothingBuilder()


_NOTHING_BUILDER = (_nothing_builder, "Do nothing.")


def _no_build_check(configuration, error_fn):
    for component_name in configuration.components():
        component = configuration.get(component_name)
        if "build" not in component:
            error_fn("No builder declared in {}".format(component_name))


def _make_builder(current_target):
    """
    Create and return a Builder for a component.

    Arguments
    component - The component the builder should be created for.
    """
    return devpipeline_core.toolsupport.tool_builder(
        current_target["current_config"], "build", devpipeline_build.BUILDERS,
        current_target)


def _find_folder(file, path):
    for root, dirs, files in os.walk(path):
        del dirs
        if file in files:
            # return os.path.join(root, file)
            return root
    return ""


def _find_file_paths(component, install_path):
    def _split_val(val):
        index = val.find('=')
        return (val[:index], val[index + 1:])

    for val in component.get_list('build.artifact_paths'):
        key, required = _split_val(val)
        found_path = _find_folder(required, install_path)
        component.set("dp.build.artifact_path.{}".format(key), found_path)


def build_task(current_target):
    """
    Build a target.

    Arguments
    target - The target to build.
    """

    target = current_target["current_config"]
    build_path = target.get("dp.build_dir")
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    try:
        builder = _make_builder(current_target)
        builder.configure(target.get("dp.src_dir"), build_path)
        builder.build(build_path)
        if "no_install" not in target:
            install_path = target.get(
                "install_path", fallback="install")
            builder.install(build_path, install_path)
            _find_file_paths(target, os.path.join(build_path, install_path))
    except devpipeline_core.toolsupport.MissingToolKey as mtk:
        current_target["executor"].warning(mtk)
