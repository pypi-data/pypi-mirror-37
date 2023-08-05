# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

__author__ = "flow.gunso@gmail.com"


def remove_empty_directories(path, level=0):
    """Recursively remove empty directories.

    Iterate on all the directories bottom-up in a path.
    Remove the directories with an empty os.listdir().

    :param path: The path to remove directories from.
    :param level: Current recursion level, provide root path validation.
    """
    import os
    from pathlib import Path

    # Check for a valid root path only.
    if level is 0:
        try:
            path = Path(path)
        except Exception as e:
            raise e

    # Actual removal.
    for p in path.iterdir():
        if p.is_dir():
            remove_empty_directories(p, level=level+1)
            if not os.listdir(str(p)):
                p.rmdir()


def is_existing_directory(path):
    """Check if a path exist and is a directory.

    :param path: The path to check.
    """
    from pathlib import Path

    path = Path(path)
    if path.exists():
        if path.is_dir():
            return True
        else:
            return False
    else:
        return False
