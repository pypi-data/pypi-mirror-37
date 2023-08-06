import os

from .core import get_year_dirs, get_loxfile_data, get_loxfiles
from .exceptions import LineNotFoundException, EmptyLineNotFound


class PFMachineData:
    def __init__(self, rootdir, serial):
        self.rootdir = rootdir
        self.serial = serial
        self.path = os.path.join(rootdir, serial)

    def get_year_dirs(self):
        return get_year_dirs(self.path)

    def get_loxfiles(self, year):
        return get_loxfiles(os.path.join(self.path, str(year)))

    def get_loxfile_data(self, year, loxfile):
        return get_loxfile_data(os.path.join(self.path, str(year), loxfile))


class Base:
    """
    Base class for data extractors. The deal is, LOX files do actually pack
    multiple spreadsheet data into one CSV file, so in order to extract everything
    cleanly...
    """

    def __init__(self, data):
        self.data = data


class CSVBase(Base):

    def get_empty_row_no(self, start=0, exception=True):
        """
        Get the first empty row number in self.data, starting from *start*
        :param start:
        :return:
        """
        no = start
        while no < len(self.data):
            row = self.data[no]
            if len(row) == 0:
                return no
            no += 1
        if exception:
            raise EmptyLineNotFound(start)

    def get_line_starting_with_no(self, s, start=0, exception=True):
        """
        Get the line number of the row, that starts with string *s*
        :param s:
        :param start:
        :return:
        """
        no = start
        while no < len(self.data):
            row = self.data[no]
            if len(row):
                if row[0].startswith(s):
                    return no
            no += 1

        if exception:
            raise LineNotFoundException((s, start))


class MetricsMixin:
    def get_metrics(self):
        """Get data from the beginning untill the first empty row"""
        return [x[0].split(": ", 1) for x in self.data[0:self.get_empty_row_no()]]


class IndexMixin:
    def get_header(self):
        return self.data[self.get_line_starting_with_no("Index")]

    def get_data(self):
        d = self.get_line_starting_with_no("Index") + 1
        return [x for x in self.data[d:] if x]


class IndexBase(IndexMixin, MetricsMixin, CSVBase):
    pass


class CalibrationPressureData(IndexBase):
    data_label = "User events"
    label = "Calibration pressure data"

    def get_data(self):
        cd = self.get_line_starting_with_no("Pressure:") + 1
        return self.data[cd:self.get_line_starting_with_no("Scale:")]

    def get_header(self):
        return self.data[self.get_line_starting_with_no("Pressure:")]


class CalibrationScaleData(IndexBase):
    data_label = "User events"
    label = "Calibration scale data"

    def get_data(self):
        cd = self.get_line_starting_with_no("Scale:") + 1
        return self.data[cd:self.get_empty_row_no(cd)]

    def get_header(self):
        return self.data[self.get_line_starting_with_no("Scale:")]


class RepositioningData(IndexBase):
    data_label = "User events"
    label = "Repositioning data"

    def get_header(self):
        rd = self.get_line_starting_with_no("Repositioning data:")
        return self.data[rd]

    def get_data(self):
        rd = self.get_line_starting_with_no("Repositioning data:") + 1
        return [x for x in self.data[rd:self.get_empty_row_no(rd)]]


class UserEvents(IndexBase):
    """This class can extract data out of User events (PLE)
    part of the LOX file"""

    data_label = "User events"
    label = "User events"

    def get_header(self):
        return super(UserEvents, self).get_header() + ["Extra #1"]


class SystemEvents(Base):
    label = "System events"

    def get_header(self):
        return ["Time", "Event"]

    def get_data(self):
        no = 0
        while no < len(self.data) - 1:
            yield self.data[no], self.data[no + 1]
            no += 2


class PLC(IndexBase):
    label = "PLC"
    pass


class PLI(IndexBase):
    label = "PLI"
    pass


class PLL(IndexBase):
    label = "PLL"
    pass


class Tare(IndexBase):
    label = "Tare"
    pass


class Fluids(IndexBase):
    label = "Fluids"
    pass


data_classess = [
    UserEvents,
    CalibrationPressureData,
    CalibrationScaleData,
    RepositioningData,
    SystemEvents,
    PLC, PLI, PLL, Tare,
    Fluids,
]
