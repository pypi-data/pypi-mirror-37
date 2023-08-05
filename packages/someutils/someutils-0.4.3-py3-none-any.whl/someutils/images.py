# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging


def is_image(path):
    """Check if a path is a valid image file

    :param path: The path to check.
    """
    from PIL import Image
    from pathlib import Path

    path = Path(path)
    try:
        i = Image.open(path)
        i.close()
        return True
    except Exception as e:
        raise e


def get_tag(path, tag):
    """Search then return a specific Exif tag.

    :param path: The file to read Exif tags from.
    :param tag: The tag to search for.
    """
    import exifread
    from pathlib import Path
    logging.getLogger("exifread").setLevel(logging.CRITICAL)

    path = Path(path)
    with open(str(path), 'rb') as file:
        tags = exifread.process_file(file, details=False, stop_tag=tag)
        if tag in tags.keys():
            return tags[tag]
        else:
            return None
