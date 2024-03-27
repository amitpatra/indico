# This file is part of Indico.
# Copyright (C) 2002 - 2024 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

import sys
from importlib.util import find_spec
from pathlib import Path

import pkg_resources


def package_is_editable(package):
    """Check whether the Python package is installed in 'editable' mode."""
    # based on pip.dist_is_editable
    dist = pkg_resources.get_distribution(package)
    for path_item in sys.path:
        if (Path(path_item) / f'{dist.project_name}.egg-link').is_file():
            return True
        if any(Path(path_item).glob(f'__editable__.{dist.project_name}-*.pth')):
            return True
    return False


def get_package_root_path(import_name):
    """Get the root path of a package.

    Returns ``None`` if the specified import name is invalid or
    points to a module instead of a package.
    """
    spec = find_spec(import_name)
    if spec is None or not spec.parent:
        # no parent if it's not a package (PEP 451)
        return None
    paths = spec.submodule_search_locations
    assert len(paths) == 1
    return paths[0]
