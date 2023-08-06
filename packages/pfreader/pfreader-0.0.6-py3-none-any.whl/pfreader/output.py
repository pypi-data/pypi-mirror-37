"""
PFReader output module

Uses tablib
"""

from pfreader.pfreader import data_classess
from . import exceptions


def get_output(lox_data):
    for elem in data_classess:
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
            headers = d.get_header()

        if headers is None:
            if not elem.required:
                continue
            raise exceptions.HeaderNotFound(elem.label)

        rowlen = len(headers)

        data = []
        if hasattr(d, "get_data"):
            for row in d.get_data():
                while len(row) < rowlen:
                    row += [""]
                data.append(row[:rowlen])
        yield (elem.label, headers, data)


def get_openpyxl(lox_data):
    import openpyxl

    wb_out = openpyxl.Workbook()
    idx = 0
    for elem, header, data in lox_data:
        ws_out = wb_out.create_sheet(elem, idx)
        idx += 1
        ws_out.append(header)
        ws_out.freeze_panes = 'A2'
        for row in data:
            ws_out.append(row)

        for column_cells in ws_out.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            ws_out.column_dimensions[column_cells[0].column].width = length

    return wb_out


def get_databook(lox_data):
    import tablib

    db = tablib.Databook()
    for label, headers, data in get_output(lox_data):
        ds = tablib.Dataset(title=label)
        ds.headers = headers
        for elem in data:
            ds.append(elem)
        db.add_sheet(ds)
    return db
