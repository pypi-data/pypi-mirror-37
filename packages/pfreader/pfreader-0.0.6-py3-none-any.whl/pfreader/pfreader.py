import os

from dateutil import parser

from . import const
from .__version__ import VERSION
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

    required = True

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

    required = False  # Older software won't dump this data

    def get_header(self):
        rd = self.get_line_starting_with_no("Repositioning data:", exception=False)
        if rd:
            return self.data[rd]

    def get_data(self):
        rd = self.get_line_starting_with_no("Repositioning data:", exception=False) + 1
        return [x for x in self.data[rd:self.get_empty_row_no(rd)]]


class UserEvents(IndexBase):
    """This class can extract data out of User events (PLE)
    part of the LOX file"""

    data_label = "User events"
    label = "User events"

    def get_header(self):
        return super(UserEvents, self).get_header() + ["Extra #1"]


class Summary(UserEvents):
    label = "Summary"

    def get_header(self):
        return ["Description", "Value"]

    def get_data(self):
        # Index, Time, Class(cod), Class, Type(cod), Type, Sample(cod), Sample, ...

        data = super(Summary, self).get_data()
        for elem in data:
            elem[2] = int(elem[2])
            elem[4] = int(elem[4])
            elem[6] = int(elem[6])

        def find_events(event, sample_cod=None):
            for elem in data:
                if elem[2] == event[0] and elem[4] in event[1]:
                    if sample_cod is not None:
                        if elem[const.SAMPLE_COD] != sample_cod:
                            continue
                    yield elem

        def count(events):
            if events is None:
                return 0
            return len(list(events))

        def first(events):
            for elem in events:
                return elem

        def last(events):
            elem = None
            for elem in events:
                pass
            return elem

        try:
            ts = first(find_events(const.EVENT_THERAPY_START))[1]
        except TypeError:
            ts = None

        yield ("Therapy start", ts or "unknown")

        try:
            te = last(find_events(const.EVENT_THERAPY_END))[1]
            yield ("Therapy end", te)
            yield ("Therapy ended", "as planned")
        except TypeError:
            try:
                te = last(find_events(const.EVENT_GENERAL_MALFUNCTION))[1]
                yield ("Therapy end", te)
                yield ("Therapy ended", "because of system general malfunction")
            except TypeError:
                te = None
                yield ("Therapy end", "unknown")

        if te is not None and ts is not None:
            delta = parser.parse(te) - parser.parse(ts)
            yield ("Therapy duration (days)", delta.days)

        for elem in find_events(const.EVENT_FILTER_CHOSEN):
            if elem[const.SAMPLE_COD] != const.TYPE_NO_FILTER:
                yield ("Filter chosen", elem[const.SAMPLE_COD + 1])
                break

        yield ("Sets used", 1 + count(find_events(const.EVENT_CHANGE_SET, sample_cod=0)))

        if count(first(find_events(const.EVENT_CVVHDF_CHOSEN))):
            tt = "CVVHDF"
        elif count(first(find_events(const.EVENT_TPE_CHOSEN))):
            tt = "TPE"
        else:
            tt = "Unknown (please send LOX file to package author)"
        yield ("Therapy type", tt)

        if tt == "CVVHDF":
            if count(find_events(const.EVENT_CITRATE_CHOSEN)):
                yield ("Anticoagulation", "citrate")

            try:
                yield ("Calcium concentration (syringe)",
                       first(find_events(const.EVENT_CALCIUM_CONCENTRATION_SYRINGE))[const.SAMPLE_COD + 1])
            except TypeError:
                pass

            try:
                yield ("Calcium concentration (substitute)",
                       first(find_events(const.EVENT_CALCIUM_CONCENTRATION_SUBSTITUTE))[const.SAMPLE_COD + 1])
            except TypeError:
                pass

            try:
                yield ("Citrate solution",
                       first(find_events(const.EVENT_CITRATE_CHOSEN))[const.SAMPLE_COD + 1])
            except TypeError:
                pass

        elif tt == "TPE":
            try:
                yield ("Plasma exchange planned", first(find_events(const.EVENT_PLASMA_VOLUME_SET))[const.SAMPLE_COD + 1])
            except TypeError:
                pass
            yield ("PBP bag volume", first(find_events(const.EVENT_SUBSTITUTE_VOLUME_SET))[const.SAMPLE_COD + 1])

        try:
            yield ("Syringe volume", first(find_events(const.EVENT_SYRINGE_SIZE_SET))[const.SAMPLE_COD + 1])
        except TypeError:
            pass

        yield ("Syringe changes", count(find_events(const.EVENT_SYRINGE_CHANGED, sample_cod=0)))
        yield ("PBP bag changes", count(find_events(const.EVENT_CHANGE_PBP, sample_cod=0)))
        yield ("Dialysate bag changes", count(find_events(const.EVENT_CHANGE_DIALYSATE, sample_cod=0)))
        yield ("Substitute bag changes", count(find_events(const.EVENT_CHANGE_SUBSTITUTE, sample_cod=0)))

        yield ("Reminder", "Generated by alpha quality software coming without ANY WARRANTY. ")
        yield ("Warning", "Values above MAY BE INACCURATE.")
        yield ("Please", "Consult the next sheet (User events) in case of any discrepancy.")
        yield ("Generated by", "pfreader version %s" % VERSION)
        yield ("Please visit", "http://github.com/mpasternak/pfreader/")


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


class Pressure(IndexBase):
    label = "Pressure"
    required = False
    pass


class Syringe(IndexBase):
    label = "Syringe"
    required = False
    pass


class PLL(IndexBase):
    label = "PLL"
    required = False
    pass


class Tare(IndexBase):
    label = "Tare"
    pass


class Fluids(IndexBase):
    label = "Fluids"
    pass


data_classess = [
    Summary,
    UserEvents,
    Pressure,
    Syringe,
    Fluids,
    Tare,
    PLC, PLI, PLL,
    CalibrationPressureData,
    CalibrationScaleData,
    RepositioningData,
    SystemEvents,
]
