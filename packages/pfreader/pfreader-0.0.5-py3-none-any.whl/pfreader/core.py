import csv
import os
import tarfile
from io import StringIO

from .const import MAX_YEAR, MIN_YEAR
from .exceptions import UnknownExtensionException


def get_loxfiles(path):
    for y_root, y_dirs, y_files in os.walk(path):
        for f_elem in y_files:
            if f_elem.lower().endswith(".lox"):
                yield f_elem


def get_year_dirs(path):
    # In the path given, find subdirectories named like years
    # eg. "2018", "2017"...
    for s_root, s_dirs, s_files in os.walk(path):
        for elem in s_dirs:
            try:
                y = int(elem)
            except (TypeError, ValueError):
                continue

            if y < MIN_YEAR or y > MAX_YEAR:
                continue

            # Those "year" subdirectories should contain files with .lox
            # extension, if there is at least one file, this is a "year"
            # directory and should be yielded:
            for _ign in get_loxfiles(os.path.join(s_root, elem)):
                yield y
                break

        # Only one level deep
        break


def get_machines(path):
    """
    Return serial NOs of PrismaFlex® machines in given path.

    PrismaFlex® directory with exported historical data looks like:
    [serial number of the machine] / [year] / [examination file].LOX

    This function yields any sub-directory of *path*, that contains a
    a 4-digit directory (in range 1900-2200), that contains at least
    one file with ".LOX" extension
    """
    for root, dirs, files in os.walk(path):
        for d in dirs:
            for _ign in get_year_dirs(os.path.join(root, d)):
                yield d
                break

        # Only one level deep
        break


def dir_contains_pflex_data(path):
    """
    This function is intended to be used on root directories of mounted
    filesystems (USB stick, memory card reader) to detect if a given
    media contains any PrismaFlex® data.

    :return: boolean
    """
    for _ign in get_machines(path):
        return True
    return False




extmap = {
    "pci": ("Network config", ["ascii", "ini", "split", "strip"]),
    "pca": None,  # Some binary data, skip it
    "pcu": ("Therapy config", ["ascii", "ini", "split", "strip"]),
    "pcm": ("Machine config", ["ascii", "split"]),
    "plr": ("System events", ["ascii", "split", "strip", "noemptylines"]),
    "ple": ("User events", ["utf-16", "split", "strip", "csv"]),
    "plp": ("Pressure", ["utf-8", "split", "strip", "csv"]),
    "pls": ("Fluids", ["ascii", "split", "strip", "csv", ]),
    "ply": ("Syringe", ["ascii", "split", "strip", "csv", ]),
    "plc": ("PLC", ["ascii", "split", "strip", "csv", ]),
    "plt": ("Tare", ["ascii", "split", "strip", "csv", ]),
    "pli": ("PLI", ["ascii", "split", "strip", "csv", ]),
    "pll": ("PLL", ["ascii", "split", "strip", "csv", ])
}


def get_loxfile_data(fname):
    """
    Returns all the data contained in the loxfile

    :param fname:
    :return: dictionary
    """

    ret = {}

    tar = tarfile.open(fname, "r:gz")

    for member in tar.getnames():
        _ign, ext = map(str.lower, member.split("."))

        f = tar.extractfile(member)
        if ext in extmap:
            if extmap[ext] is None:
                continue

            desc, extra = extmap[ext]
            data = f.read()

            for elem in extra:
                if elem == "strip":
                    data = [x.strip() for x in data]
                    continue

                if elem == "split":
                    data = data.split("\n")
                    continue

                if elem in ["utf-8", "utf-16", "ascii"]:
                    data = data.decode(elem)
                    continue

                if elem == "csv":
                    data = [x for x in csv.reader(data, delimiter=';')]
                    continue

                if elem == "noemptylines":
                    data = [x for x in data if x]
                    continue

            ret[desc] = data

        else:
            raise UnknownExtensionException(ext)

    return ret
