"""Coverage plugin for pytest."""
import os
import pytest
import sys

from pytest_plugin import PytestPlugin


sys.path.append('.')


def pytest_addoption(parser):
    """Add options to control coverage."""

    group = parser.getgroup(
        'coverage', 'coverage for live test')

    group.addoption('--coverage', action='append', default=[],
                    nargs='?', const=True, dest='coverage_source',
                    help='measure coverage for filesystem path ')

    group.addoption('--coverage-config', action='store', default='.coveragerc',
                    metavar='path',
                    help='config file for coverage, default: .coveragerc')

    group.addoption('--coverage-outdir', action='store', default='coverage',
                    metavar='path',
                    help='config dir for output coverage, default: coverage')


@pytest.mark.tryfirst
def pytest_load_initial_conftests(early_config, parser, args):
    if early_config.known_args_namespace.coverage_source:
        plugin = PytestPlugin(
            early_config.known_args_namespace,
            early_config.pluginmanager
        )
        early_config.pluginmanager.register(plugin, '_coverage')
