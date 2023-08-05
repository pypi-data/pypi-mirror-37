# -*- coding: utf8 -*-
import logging
import sys
import threading

import pkg_resources
from pkg_resources import VersionConflict, DistributionNotFound

COMMON_DEPENDENCIES = [
    'ml-legit>=18.9.259',
    'diskcache>=3.0.1',
]

GCS_DEPENDENCIES = [
    'google-cloud-storage==1.6.0',
]
S3_DEPENDENCIES = [
    'boto3>=1.4.8,<1.5.0',
]

KEYWORDS = []


__pip_install_lock = threading.Lock()


def install_dependencies(dependencies, throw_exception=True):
    from missinglink.sdk.pip_util import pip_install

    running_under_virtualenv = getattr(sys, 'real_prefix', None) is not None

    needed_dependencies = []
    for requirement in dependencies:
        if _is_dependency_installed(requirement):
            continue

        needed_dependencies += [requirement]

    if not needed_dependencies:
        return

    with __pip_install_lock:
        p, args = pip_install(None, needed_dependencies, not running_under_virtualenv)

        if p is None:
            raise Exception('Failed to install requirement: %s' % needed_dependencies)

        try:
            std_output, std_err = p.communicate()
        except Exception:
            if throw_exception:
                raise

            logging.exception('%s failed', ' '.join(args))
            return False

        rc = p.returncode

        if rc != 0:
            logging.error('Failed to install requirement: %s' % needed_dependencies)
            logging.error('Failed to run %s (%s)\n%s\n%s', ' '.join(args), rc, std_err, std_output)

            if throw_exception:
                raise Exception('Failed to install requirement: %s' % needed_dependencies)

        logging.info('install requirement: %s' % needed_dependencies)
        logging.info('ran %s (%s)\n%s\n%s', ' '.join(args), rc, std_err, std_output)


def _is_dependency_installed(requirement):
    try:
        pkg_resources.require(requirement)
    except (IOError, DistributionNotFound, VersionConflict):
        return False

    return True
