#!/usr/bin/python3

"""
Main module for devpipeline_scm.  It provides SCMS, a dictionary with all
detected scm plugins.
"""

import devpipeline_core.plugin

SCMS = devpipeline_core.plugin.query_plugins('devpipeline.scms')


class _SimpleScm(devpipeline_core.toolsupport.SimpleTool):

    """This class is a simple SCM tool."""

    def __init__(self, real, current_target):
        super().__init__(current_target, real)

    def checkout(self, repo_dir):
        """This function checks out source code."""
        self._call_helper("Checking out", self.real.checkout,
                          repo_dir)

    def update(self, repo_dir):
        """This funcion updates a checkout of source code."""
        self._call_helper("Updating", self.real.update,
                          repo_dir)


def make_simple_scm(real_scm, configuration):
    """
    Create an Scm instance that leverages executors.

    Arguments:
    real_scm - a class instance that provides an Scm interface
    configuration - the configuration for the Scm target
    """
    return _SimpleScm(real_scm, configuration)
