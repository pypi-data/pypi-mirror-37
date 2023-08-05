from PyQt4.QtCore import QObject, pyqtSignal

from .slicemodel import SliceDirection
import numpy as np
import segyio
import os


class EmptyDataSource(object):
    def __init__(self):
        super(EmptyDataSource, self).__init__()
        self._data = np.zeros((2, 2), dtype=np.single)
        self._data[0, 0] = -1.0
        self._data[1, 1] = 1.0
        self._xlines = [0, 1]
        self._ilines = [0, 1]
        self._samples = []  # changed to allow dims() calculate len(samples)

    @property
    def ilines(self):
        return self._ilines

    @ilines.setter
    def ilines(self, value):
        self._ilines = value

    @property
    def xlines(self):
        return self._xlines

    @xlines.setter
    def xlines(self, value):
        self._xlines = value

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = value

    @property
    def iline(self):
        return [self._data, self._data]

    @property
    def xline(self):
        return [self._data, self._data]

    @property
    def iline(self):
        return [self._data, self._data]

    @property
    def depth_slice(self):
        return [self._data, self._data]

    @property
    def sorting(self):
        return segyio.TraceSortingFormat.CROSSLINE_SORTING


class SliceDataSource(QObject):
    slice_data_source_changed = pyqtSignal()

    def __init__(self, filename, **kwargs):
        QObject.__init__(self)

        self._file_size = 0
        self._source = None
        """ :type: segyio.SegyFile """
        self.set_source_filename(filename, **kwargs)
        self._source_filename = filename

    def _close_current_file(self):
        self._file_size = 0

        if self._source is None: return

        try: self._source.close()
        except AttributeError: pass

        self._source = None

    @property
    def file_size(self):
        return self._file_size

    @property
    def source_filename(self):
        return self._source_filename

    def set_source_filename(self, filename, **kwargs):
        if filename:
            try:
                file_size = os.stat(filename).st_size
                source = segyio.open(filename, "r", **kwargs)
                self._source_filename = filename
            except:
                raise
            else:
                self._close_current_file()
                self._source = source
                self._file_size = file_size
                self._source.mmap()
                samples = self._source.samples
        else:
            self._close_current_file()
            self._source = EmptyDataSource()

        self.slice_data_source_changed.emit()

    def read_slice(self, direction, index):
        if direction == SliceDirection.inline:
            iline_index = self._source.ilines[index]
            return self._source.iline[iline_index].T
        elif direction == SliceDirection.crossline:
            xline_index = self._source.xlines[index]
            return self._source.xline[xline_index].T
        elif direction == SliceDirection.depth:
            data = self._source.depth_slice[index]
            if self._source.sorting == segyio.TraceSortingFormat.CROSSLINE_SORTING:
                return data
            else:
                return data.T
        else:
            raise ValueError("Unknown direction: %s" % direction)

    def indexes_for_direction(self, direction):
        if direction == SliceDirection.inline:
            return self._source.ilines
        elif direction == SliceDirection.crossline:
            return self._source.xlines
        elif direction == SliceDirection.depth:
            return self._source.samples
        else:
            raise ValueError("Unknown direction: %s" % direction)

    def __del__(self):
        self._close_current_file()

    def dims(self):
        iline_count = len(self._source.ilines)
        xline_count = len(self._source.xlines)
        offset_count = 1
        sample_count = len(self._source.samples)
        return iline_count, xline_count, offset_count, sample_count

    def set_indexes(self, direction, values):
        if direction == SliceDirection.inline:
            self._source.ilines = values
        elif direction == SliceDirection.crossline:
            self._source.xlines = values
        elif direction == SliceDirection.depth:
            self._source.samples = values
        else:
            raise ValueError("Unknown direction: %s" % direction)
