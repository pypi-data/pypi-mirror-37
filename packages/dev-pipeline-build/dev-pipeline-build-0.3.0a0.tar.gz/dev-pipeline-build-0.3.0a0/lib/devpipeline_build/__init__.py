#!/usr/bin/python3

"""
Root module for the build plugin.  It provides the BUILDERS dictionary, which
contains every builder plugin.
"""

import devpipeline_core.plugin

BUILDERS = devpipeline_core.plugin.query_plugins('devpipeline.builders')


class _SimpleBuild(devpipeline_core.toolsupport.SimpleTool):

    """This class does a simple build - configure, build, and install."""

    def __init__(self, real, current_target):
        super().__init__(current_target, real)

    def configure(self, src_dir, build_dir):
        # pylint: disable=missing-docstring
        self._call_helper("Configuring", self.real.configure,
                          src_dir, build_dir)

    def build(self, build_dir):
        # pylint: disable=missing-docstring
        self._call_helper("Building", self.real.build,
                          build_dir)

    def install(self, build_dir, path=None):
        # pylint: disable=missing-docstring
        self._call_helper("Installing", self.real.install,
                          build_dir, path)


def make_simple_builder(real_builder, configuration):
    """
    Create an Build instance that leverages executors.

    Arguments:
    real_builder - a class instance that provides an Build interface
    configuration - the configuration for the Build target
    """
    return _SimpleBuild(real_builder, configuration)
