"""
PFReader output module

Uses tablib
"""

import tablib

from pfreader.pfreader import data_classess
from . import exceptions


def get_databook(lox_data):
    db = tablib.Databook()
    for elem in data_classess:
        ds = tablib.Dataset(title=elem.label)

        try:
            if hasattr(elem, "data_label"):
                data = lox_data[elem.data_label]
            else:
                data = lox_data[elem.label]
        except KeyError:
            if not elem.required:
                continue
            raise exceptions.DataNotFound(elem.label)

        d = elem(data)

        if hasattr(d, "get_header"):
            ds.headers = d.get_header()

        if ds.headers is None:
            if not elem.required:
                continue
            raise exceptions.HeaderNotFound(elem.label)

        rowlen = len(ds.headers)

        if hasattr(d, "get_data"):
            for elem in d.get_data():
                while len(elem) < rowlen:
                    elem += [""]

                ds.append(elem[:rowlen])
            # map(ds.append, d.get_data())
        db.add_sheet(ds)
    return db
