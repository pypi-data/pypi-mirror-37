#!/usr/bin/env python
import re
import uuid

VERISK_FILE = '/etc/verisk'


def verisk(VERISK_FILE=VERISK_FILE):
    """
    Get the verisk ID from the specified file. If the file is unreadable for
    some reason (perhaps it doesn't exist), this will return None. However, if
    the first line of the file is not a UUID, we decide the file contains other
    things besides a verisk ID and raise a ValueError.
    """
    res = None
    try:
        f = open(VERISK_FILE, "r")
        for line in f:
            if re.match("[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", line.strip()) is not None:
                res = line.strip()
            else:
                # this is not a verisk file!
                raise ValueError(
                    "The specified file doesn't appear to contain a verisk.")
        f.close()
    except IOError as e:
        pass  # if we can't read the file for some reason, we assume there is no file
    return res


def _write_new_id(VERISK_FILE=VERISK_FILE):
    """
    Unsafe! This erases the existing ID.
    """
    verisk_id = str(uuid.uuid4())
    f = open(VERISK_FILE, "w")
    f.write(verisk_id + "\n")
    f.close()
    return verisk_id


def make_verisk(VERISK_FILE=VERISK_FILE):
    """
    If a verisk ID exists, returns it. Otherwise, creates one.
    """
    if not verisk(VERISK_FILE):
        _write_new_id(VERISK_FILE)
    return verisk(VERISK_FILE)
