# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from itertools import chain, groupby
from math import ceil, floor

import declxml as xml
import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta
from matplotlib.widgets import CheckButtons, Slider
from mpl_toolkits.mplot3d.proj3d import proj_transform

try:
    import itertools.imap as map
    import itertools.izip as zip
except ImportError:
    pass


def segmentsToCoord(segm, coord, coords, scaleFactor, nFrames=None):
    """ Extracts a single coordinate from a segment string"""
    index = coords.index(coord)
    a = segm.split('S ')[1:]
    b = (list(map(int, i.rstrip().split(' '))) for i in a)
    c = [(i[0], [j / scaleFactor for j in i[1:][index::len(coords)]])
         for i in b]

    if nFrames:
        arr = [None] * nFrames
    else:
        arr = [None] * len(c[0][1])

    for start, value in c:
        end = start + len(value)
        if end > len(arr):
            raise Exception("Out of bounds")
        arr[start:start + len(value)] = value
    return arr


def depth(g, count=0):
    return count if not isinstance(g, list) else max([depth(x, count+1) for x in g])


def coordToSegments(coords, scaleFactor):
    if depth(coords) > 1:
        co = zip(*coords)
    else:
        co = zip(coords)
    """Converts an array of coords [[X], [Y], [Z]] into a segmented
    string "S 0 X1 Y1 Z1". It generates as many segments as required"""

    g = [list(v) for i, v in groupby(enumerate(co),
                                     key=lambda x: x[1][0] in [None, np.NaN]) if not i]
    ta = [(i[0][0], map(lambda x: x[1], i)) for i in g]
    fa = ['S {} {}'.format(i[0], ' '.join(str(int(j * scaleFactor))
                                          for sub in i[1] for j in sub)) for i in ta]
    return ' '.join(fa)


class mdxItem(object):
    def __init__(self, data=None, coords=None, scaleFactor=None, nFrames=None):

        if isinstance(data, basestring):
            if data.startswith('S '):
                self._coords = coords
                self._scaleFactor = scaleFactor
                self._segmented = True
                self._nFrames = nFrames
                self._data = data
            else:
                self._coords = coords
                self._scaleFactor = scaleFactor
                self._segmented = False
                self._nFrames = nFrames
                self._data = data

    def __getattr__(self, coord):
        if coord in self._coords:
            index = self._coords.index(coord)
            if self._segmented:
                j = segmentsToCoord(
                    self._data, index, self.coords, self._scaleFactor, self._nFrames)
            else:
                j = [int(i) / self._scaleFactor for i in self._data.rstrip().split(' ')
                     [index::len(self._coords)]]
            if len(j) == 1:
                return j[0]
            return j
        raise KeyError(coord)

    def __setattr__(self, coord, value):
        if coord == '_coords':
            self.__dict__[coord] = value
        elif coord in self._coords:
            # If it's a single segment, assign its coordinate
            if self._segmented and len(self._data) == 1:
                setattr(self._data[0], coord, value)
            else:
                # Check it's the same length as the other coords
                if not isinstance(value, list):
                    value = [value]
                index = self._coords.index(coord)
                self._data[index::len(self._coords)] = value
        else:
            super(mdxItem, self).__setattr__(coord, value)

    def append(self, data, coords=None, scaleFactor=None):
        # if isinstance(data, mdxSegment):
        #     if not self._segmented:
        #         raise Exception(
        #             'Cannot append a segment to a non segmented mdxItem')
        #     if data._scaleFactor != self._scaleFactor:
        #         raise Exception(
        #             'Cannot append a segment with a different scaleFactor')
        #     if data._coords != self._coords:
        #         raise Exception(
        #             'Cannot append a segment with different coords')
        #     if data._startFrame in [i._startFrame for i in self._data]:
        #         raise Exception(
        #             'Cannot append segment: two segments
        # with the same startFrame')
        #     self._data.append(data)
        #     self._coords = data._coords
        #     self._scaleFactor = data._scaleFactor
        if isinstance(data, list):
            if self._segmented:
                raise Exception(
                    'Cannot only append a segment to a segmented mdxItem')
            if scaleFactor != self._scaleFactor:
                raise Exception(
                    'Cannot append data with different scaleFactor')
            if coords != self._coords:
                raise Exception(
                    'Cannot append data with different coords')
            self._data.extend(data)

    @property
    def data(self):
        if self._segmented:
            r = [segmentsToCoord(self._data, index, self._coords,
                                 self._scaleFactor, self._nFrames) for index in self._coords]
        else:
            r = [getattr(self, coord) for coord in self._coords]

        if len(r) == 1:
            return r[0]
        return r

    def serialize(self):
        if self._segmented:
            d = [i.serialize() for i in self._data]
        else:
            d = [str(int(i * self._scaleFactor)) for i in self._data]
        return 'I {}'.format(' '.join(d))


class mdxTrial(object):
    """docstring for mdxTrial"""

    def __init__(self):
        self._date = None
        self._description = None
        self._label = None
        self._time = None

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = str(value)        

    @property
    def date(self):
        return datetime.strptime(self._date, "%d-%m-%Y").date()

    @date.setter
    def date(self, newdate):
        self._date = newdate.strftime("%d-%m-%Y")
        print(newdate, self._date)

    @property
    def time(self):
        return datetime.strptime(self._time, "%H:%M:%S").time()

    @time.setter
    def time(self, newtime):
        self._time = newtime.strftime("%H:%M:%S")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value)

    @property
    def markerStream(self):
        # Marker stream is the first stream that has a track labeled 'c7' on it
        for i, v in enumerate(self.streams):
            if v.type == 'markerStream':
                return self.streams[i]
        raise KeyError("No marker stream present")

    @property
    def forceStream(self):
        # Force stream is the first stream that has a force tag on it
        for i, v in enumerate(self.streams):
            if v.type == 'forceStream':
                return self.streams[i]
        raise KeyError("No force stream present")

    @property
    def emgStream(self):
        # emg stream is the first stream that has an emg tag on it
        for i, v in enumerate(self.streams):
            if v.type == 'emgStream':
                return self.streams[i]
        raise KeyError("No emg stream present")

    @property
    def static(self):
        return self._static

    @static.setter
    def static(self, value):
        if isinstance(value, mdxStatic):
            self._static = value


class mdxCycle(object):
    """docstring for mdxCycle"""

    def __init__(self):
        self._frequency = None
        self._description = None
        self._label = None
        self._startTime = None

    @property
    def scalar_bands(self):
        return {i.label: i for i in self._scalar_bands}

    @scalar_bands.setter
    def scalar_bands(self, value):
        if isinstance(value, dict):
            self._scalar_bands = value.values()
        elif isinstance(value, list):
            self._scalar_bands = value

    @property
    def scalars(self):
        return {i.label: i for i in self._scalars}

    @property
    def angles(self):
        return {i.label: i for i in self._angles}

    @scalars.setter
    def scalars(self, value):
        if isinstance(value, dict):
            self._scalars = value.values()
        elif isinstance(value, list):
            self._scalars = value


class mdxStream(object):
    """docstring for mdxTrial"""

    def __init__(self):
        self._frequency = None
        self._description = None
        self._label = None
        self._startTime = None
        self._nFrames = None

    @property
    def frequency(self):
        return float(self._frequency)

    @frequency.setter
    def frequency(self, value):
        self._frequency = str(value)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = str(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value)

    @property
    def startTime(self):
        return int(self._startTime)

    @startTime.setter
    def startTime(self, value):
        self._startTime = str(value)

    @property
    def tracks(self):
        for i in self._tracks:
            setattr(i, '_nFrames', self._nFrames)
        return {i.label: i for i in self._tracks}

    @property
    def forces(self):
        for i in self._forces:
            setattr(i, '_nFrames', self._nFrames)
        return {i.label: i for i in self._forces}

    @property
    def torques(self):
        for i in self._torques:
            setattr(i, '_nFrames', self._nFrames)
        return {i.label: i for i in self._torques}

    @property
    def powers(self):
        for i in self._powers:
            setattr(i, '_nFrames', self._nFrames)
        return {i.label: i for i in self._powers}

    @property
    def references(self):
        for i in self._references:
            setattr(i, '_nFrames', self._nFrames)
        return {i.label: i for i in self._references}

    @tracks.setter
    def tracks(self, value):
        if isinstance(value, dict):
            self._tracks = value.values()
        elif isinstance(value, list):
            self._tracks = value

        self._nFrames = self._tracks[0]._nFrames

    @property
    def type(self):
        """Returns the type of stream"""
        if hasattr(self, '_forces') and self._forces:
            logging.info("forceStream found")
            return "forceStream"
        if hasattr(self, '_emg') and self._emg:
            logging.info("emgStream found")
            return "emgStream"
        if any(j.label in ['c7', 'N', 'TCO'] for j in self._tracks):
            return "markerStream"
        raise Exception("Unknown stream")

    def plot(self, *args, **kwargs):
        if self.type == 'markerStream':
            self._plotMarkers(*args, **kwargs)

    def _plotMarkers(self, labels=None):

        inipos = 0
        rang = self._nFrames

        ctracks_data = {label: [np.array(value.X, dtype=np.float),
                                np.array(value.Y, dtype=np.float),
                                np.array(value.Z, dtype=np.float)]
                        for label, value in self.tracks.iteritems()}
        creferences_data = {label: [np.array(value.X, dtype=np.float),
                                    np.array(value.Y, dtype=np.float),
                                    np.array(value.Z, dtype=np.float)]
                            for label, value in self.references.iteritems()}

        def update_graph(num):
            num = int(num)
            for label, value in ctracks_data.iteritems():
                X = value[0][num:1 + num]
                Y = value[1][num:1 + num]
                Z = -value[2][num:1 + num]
                if not (X[0] and Y[0] and Z[0]):
                    X[0] = Y[0] = Z[0] = 0
                    graphs[label].set_visible(False)
                    graphs[label].set_data(X, Z)
                    graphs[label].set_3d_properties(Y)
                else:
                    graphs[label].set_visible(True and check.get_status()[0])
                    graphs[label].set_data(X, Z)
                    graphs[label].set_3d_properties(Y)
            for label, value in creferences_data.iteritems():
                X = value[0][num:1 + num]
                Y = value[1][num:1 + num]
                Z = -value[2][num:1 + num]
                if not (X[0] and Y[0] and Z[0]):
                    X[0] = Y[0] = Z[0] = 0
                    rraphs[label].set_visible(False)
                    rraphs[label].set_data(X, Z)
                    rraphs[label].set_3d_properties(Y)
                else:
                    rraphs[label].set_visible(True and check.get_status()[1])
                    rraphs[label].set_data(X, Z)
                    rraphs[label].set_3d_properties(Y)
            title.set_text('3D Markers Plot, time={}'.format(
                (inipos + num) / self.frequency))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.axis('scaled')
        ax.set_xlim([-2, 2])
        ax.set_ylim([-1, 1])
        fig.tight_layout(True)

        title = ax.set_title('3D Markers Plot')

        axamp = plt.axes([0.25, .03, 0.50, 0.04])
        samp = Slider(axamp, 'Time', inipos, rang - 1, valinit=0)
        samp.on_changed(update_graph)

        rax = plt.axes([0.05, 0.4, 0.1, 0.15])
        check = CheckButtons(rax, ('markers', 'references'), (True, True))

        def func(label):
            status = check.get_status()
            for i in graphs.values():
                i.set_visible(i.get_visible() and status[0])
            for i in rraphs.values():
                i.set_visible(i.get_visible() and status[1])
            fig.canvas.draw_idle()

        check.on_clicked(func)

        graphs = {}
        rraphs = {}
        for label, value in self.tracks.iteritems():
            X = Y = Z = [0]
            g, = ax.plot(X, Z, Y, label=label,
                         linestyle="", marker="o", picker=5)
            g.set_visible(False)
            graphs[label] = g
            annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="w"),
                                arrowprops=dict(arrowstyle="->"))

            annot.set_visible(False)

        for label, value in self.references.iteritems():
            r, = ax.plot(
                X, Z, Y, label=label, linestyle="", marker="o", picker=5)
            r.set_visible(False)
            rraphs[label] = r

            annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="w"),
                                arrowprops=dict(arrowstyle="->"))

            annot.set_visible(False)

        def hover(event):
            vis = annot.get_visible()
            for curve in ax.get_lines():
                cont, ind = curve.contains(event)
                if cont and curve.get_visible():
                    annot.xy = (event.xdata, event.ydata)
                    annot.set_text(curve.get_label())
                    annot.get_bbox_patch().set_facecolor(curve.get_color())
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', hover)
        plt.show()

    def toTRC(self, filename, labels=None, startTime=None, endTime=None, trim=False, no_spaces=False):
        """ Converts markerStream to an OpenSIM's trc file
            To avoid NaN values, the longest common chunk is used """

        if not self.type == 'markerStream':
            raise Exception("toTRC only available in markerStream")

        if labels:
            items = {key: value for key,
                     value in self.tracks.iteritems() if key in labels}
        else:
            items = [np.array(i.data, dtype=np.float)
                     for i in self.tracks.values()]
            labels = self.tracks.keys()

        if no_spaces:
            labels = [i.replace(' ', '_') for i in labels]

        freq = self.frequency

        if not filename.endswith(".trc"):
            filename = filename + ".trc"

        firstFrame = 0
        lastFrame = self._nFrames - 1

        if trim:
            for fre in range(lastFrame):
                if not any(i[0][fre] for i in items if np.isnan(i[0][fre])):
                    break
            firstFrame = fre
            print("Firstframe: ", fre)

            for las in range(firstFrame, lastFrame):
                if any(i[0][las] for i in items if np.isnan(i[0][las])):
                    break
            lastFrame = las - 1

            # while
            # for item in items:
            #     print index, np.isnan(item)[0]

        """ Check that startTime and endTime are contained in the longest common chunk.
            Raise an error otherwise"""

        if startTime:
            firstFrame = int(floor(startTime * freq)) - 1

        if endTime:
            lastFrame = int(ceil(endTime * freq)) + 1

        nrows = lastFrame - firstFrame + 1
        units = 'm'

        # Starting header generation

        header1 = ['PathFileType', '4', '(X/Y/Z)', os.path.basename(filename)]
        trc_header = []
        trc_header.append('\t'.join(header1) + '\n')

        header2 = ['DataRate', 'CameraRate',
                   'NumFrames', 'NumMarkers',
                   'Units', 'OrigDataRate',
                   'OrigDataStartFrame', 'OrigNumFrames']

        trc_header.append('\t'.join(header2) + '\n')

        header3 = [str(freq), str(freq), str(nrows), str(len(items)),
                   str(units), str(freq), str(firstFrame), str(lastFrame)]
        trc_header.append('\t'.join(header3) + '\n')

        header4 = ['Frame#', 'Time', '\t\t\t'.join(labels)]
        trc_header.append('\t'.join(header4) + '\n')

        header5 = ['X' + str(x + 1) + '\tY' + str(x + 1) + '\tZ' +
                   str(x + 1) + '\t' for x, y in enumerate(labels)]
        trc_header.append('\t\t' + "".join(header5) + '\n')

        def l(x):
            if x:
                return str(x)
            return "NaN"

        def linewriter():
            """ Data line generator """
            f = firstFrame
            while f <= lastFrame:
                frameAndTime = "{}\t{:.2f}".format(f, f / freq)
                gen = ("{:.4f}\t{:.4f}\t{:.4f}".format(
                    i[0][f], i[1][f], i[2][f]) for i in items)
                xyz = "\t".join(gen)
                fa = "{}\t{}\n".format(frameAndTime, xyz)
                yield fa
                f = f + 1

        lines = linewriter()

        logging.info("Writing file %s", filename)

        with open(filename, 'w') as file:
            for row in trc_header:
                file.write("%s" % row)

            for li in lines:
                file.write("%s" % li)

    def toMOT(self, filename=None, startTime=None, endTime=None, smooth=True):
        """ Converts forceStream to an OpenSIM's mot file """

        if not self.type == 'forceStream':
            raise Exception("toMOT only available in forceStream")

        if 'r gr' not in self.forces.keys() and 'l gr' not in self.forces.keys():
            raise Exception("No left or right force vectors in the trial.")

        forces = self.forces
        pressure = self.tracks
        torques = self.torques

        ini = []

        header2 = ['time']

        right = 'r gr s' if smooth else 'r gr'
        left = 'l gr s' if smooth else 'l gr'

        if right in forces.keys():
            ini.extend(forces[right].data)
            header2.extend(['ground_forceR_v{}'.format(i) for i in 'xyz'])
            ini.extend(pressure[right].data)
            header2.extend(['ground_forceR_p{}'.format(i) for i in 'xyz'])

        if left in forces.keys():
            ini.extend(forces[left].data)
            header2.extend(['ground_forceL_v{}'.format(i) for i in 'xyz'])
            ini.extend(pressure[left].data)
            header2.extend(['ground_forceL_p{}'.format(i) for i in 'xyz'])

        if right in forces.keys():
            ini.extend(torques[right].data)
            header2.extend(['ground_torqueR_{}'.format(i) for i in 'xyz'])

        if left in forces.keys():
            ini.extend(torques[left].data)
            header2.extend(['ground_torqueL_{}'.format(i) for i in 'xyz'])

        firstFrame = 0
        lastFrame = self._nFrames - 1

        freq = self.frequency

        if not filename.endswith(".mot"):
            filename = filename + ".mot"

        """ Check that startTime and endTime are contained in the longest common chunk.
            Raise an error otherwise"""

        if startTime:
            firstFrame = int(floor(startTime * freq)) - 1

        if endTime:
            lastFrame = int(ceil(endTime * freq)) + 1

        nrows = lastFrame - firstFrame + 1
        units = 'm'

        ncols = len(ini) + 1

        header1 = [os.path.basename(filename),
                   'Version=1',
                   'nRows={}'.format(nrows),
                   'nColumns={}'.format(ncols),
                   'inDegrees=yes',
                   'endheader']

        mot_header = '\n'.join(header1) + '\n' + '\t'.join(header2) + '\n'

        def l(x):
            if x:
                return str(x)
            return 0

        def linewriter():
            """ Data line generator """
            f = firstFrame
            while f <= lastFrame:
                frameAndTime = "{:.4f}".format(f / freq)
                row = "\t".join(["{}".format(l(i[f])) for i in ini])
                fa = "{}\t{}\n".format(frameAndTime, row)
                yield fa
                f = f + 1

        logging.info("Writing file %s", filename)
        lines = linewriter()

        with open(filename, 'w') as file:
            file.write(mot_header)

            for li in lines:
                file.write("%s" % li)


class mdxStatic(object):
    def __init__(self):
        self._frequency = None
        self._description = None
        self._label = None

    @property
    def frequency(self):
        return float(self._frequency)

    @frequency.setter
    def frequency(self, value):
        return str(value)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = str(value)

    @property
    def tracks1d(self):
        return {i.label: i for i in self._tracks1d}

    @property
    def vel1d_band(self):
        return {i.label: i for i in self._speed_bands}

    @property
    def vel1d(self):
        return {i.label: i for i in self._speeds}

    @property
    def events(self):
        return {i.label: i for i in self._events}

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value)

    @property
    def frequencies(self):
        return self._freqs

    @property
    def mass(self):
        return self._mass[0]

    @property
    def height(self):
        return self.tracks1d['dTH']

    @property
    def date(self):
        return datetime.strptime(self.texts['Session date'].data, "%d/%m/%Y").date()

    @property
    def birthday(self):
        return datetime.strptime(self.texts['Birthday'].data, "%d/%m/%Y").date()

    @property
    def age(self):
        return relativedelta(self.date, self.birthday).years

    @property
    def texts(self):
        return {i.label: i for i in self._texts}

    def add_text(self, data, label=label, IDlabel=None, description=None):
        t = mdxDataItem()
        t.label = label
        t._IDlabel = label
        t.data = data
        t.coords = 'V'
        t.nPoints = 1
        t.nItems = -1
        t.nSegs = -1
        t.scaleFactor = 1
        self._texts.append(t)


class mdxDataItem(object):
    def __init__(self):
        self._coords = None
        self._label = None
        self._IDlabel = None
        self._nItems = None
        self._nPoints = None
        self._nFrames = None
        self._nSegs = None
        self._scaleFactor = None
        self._data = None

    def __getattr__(self, coord):
        if coord in self.coords:
            if self._data.startswith('I '):
                r = [mdxItem(i, self.coords, self.scaleFactor)
                     for i in self._data.split('I ')[1:]]
                r = [getattr(i, coord) for i in r]

            elif self._data.startswith('S '):
                return segmentsToCoord(self._data, coord, self.coords, self.scaleFactor, self._nFrames)
            else:
                index = self.coords.index(coord)
                r = [int(i) / self.scaleFactor for i in self._data.rstrip().split(' ')
                     [index::len(self.coords)]]

            if len(r) == 1:
                return r[0]
            return r
        raise KeyError(coord)

    # def __setattr__(self, coord, value):
    #     if coord == '_coords':
    #         super(mdxDataItem,self).__setattr__(coord,value)
    #     if self._coords and coord in self._coords:
    #         if self._data.startswith('I '):
    #             raise Exception("Cannot set coordinates on itemized DataItem. Use item.data")
    #         elif self._data.startswith('S '):
    #             raise Exception("Cannot set coordinates on segmented DataItem. Use item.data")
    #         else:
    #             self.coord =
    #             r = [i / self.scaleFactor for i in map(int, self._data.rstrip().split(' '))]
    #             return

    #     super(mdxDataItem,self).__setattr__(coord,value)

    @property
    def scaleFactor(self):
        return self._scaleFactor

    @scaleFactor.setter
    def scaleFactor(self, value):
        self._scaleFactor = float(value)

    @property
    def nItems(self):
        return self._nItems

    @nItems.setter
    def nItems(self, value):
        self._nItems = int(value)

    @property
    def nPoints(self):
        return self._nPoints

    @nPoints.setter
    def nPoints(self, value):
        self._nPoints = int(value)

    @property
    def nSegs(self):
        return self._nSegs

    @nSegs.setter
    def nSegs(self, value):
        self._nSegs = int(value)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = unicode(value)

    @property
    def coords(self):
        return self._coords.split(" ")

    @coords.setter
    def coords(self, value):
        if isinstance(value, list):
            self._coords = " ".join(value)
        else:
            self._coords = value

    @property
    def istext(self):
        return True if self._IDlabel else False

    @property
    def data(self):
        if self.istext:
            return self._data
        if self._data.startswith('I '):
            r = [mdxItem(i, self.coords, self.scaleFactor, nFrames=self._nFrames)
                 for i in self._data.split('I ')[1:]]
        elif self._data.startswith('S'):
            r = [segmentsToCoord(self._data, coord, self.coords,
                                 self.scaleFactor, self._nFrames) for coord in self.coords]
        else:
            r = [
                i / self.scaleFactor for i in map(int, self._data.rstrip().split(' '))]

        if len(r) == 1:
            return r[0]
        return r

    def setSegments(self, value, scaleFactor=None):
        if len(value) is not len(self.coords):
            raise Exception(
                "Value has to be an array for each coordinate {}".format(self.coords))
        if not scaleFactor:
            scaleFactor = self.scaleFactor
        self._data = coordToSegments(value, scaleFactor)

    @data.setter
    def data(self, value):
        if self.istext:
            self._data = value
            return

        if isinstance(value, mdxItem):
            self._data = value.serialize()
            self.scaleFactor = value._scaleFactor
            self.coords = value._coords

        elif isinstance(value, list):
            if all(isinstance(i, mdxItem) for i in value):
                self._data = ' '.join([i.serialize() for i in value])
                self.coords = value[0]._coords
                self.scaleFactor = value[0]._scaleFactor
            else:
                self._data = coordToSegments(value, self.scaleFactor)

        elif isinstance(value, int) or isinstance(value, float):
            self._data = str(int(value * self.scaleFactor))

    # def __repr__(self):
    #     return '{}(label={}, coords={}), data={}'.format(self.__class__.__name__, self._label, self._coords, len(self._data))


class mdxParser(object):
    """docstring for mdxParser"""

    def __init__(self, filename):
        self.filename = filename
        self.parse()

    def customProcessor(self, tag_name, obj, required=True):

        base_data = [
            xml.string('.', attribute='coords', alias='_coords'),
            xml.string('.', attribute='label', alias='_label'),
            xml.integer('.', attribute='nItems', alias='_nItems'),
            xml.integer('.', attribute='nPoints', alias='_nPoints'),
            xml.integer('.', attribute='nSegs', alias='_nSegs'),
            xml.floating_point('.', attribute='scaleFactor',
                               alias='_scaleFactor'),
            xml.string('.', attribute='description',
                       alias='_description', required=False),
            xml.string('.', attribute='data', alias='_data', required=False),
            xml.string('.', attribute='IDlabel', alias='_IDlabel', required=False)]

        return xml.user_object(
            tag_name, obj, base_data, required=required)

    def parse(self):

        # stream processors

        tags_aliases = [('track', 'tracks'), ('reference', 'references'),
                        ('emg', 'emg'), ('emg_band', 'emg_bands'),
                        ('event', 'events'), ('event_band', 'event_bands'),
                        ('freq', 'freqs'), ('freq_band', 'freq_bands'),
                        ('track1d', 'tracks1d'), ('track1d_band', 'track1d_bands'),
                        ('angle', 'angles'), ('angle_band', 'angle_bands'),
                        ('angle3d', 'angles3d'), ('power', 'powers'),
                        ('power_band', 'power_bands'),
                        ('vel1d', 'speeds'), ('vel1d_band', 'speed_bands'),
                        ('scalar', 'scalars'), ('scalar_band', 'scalar_bands'),
                        ('force', 'forces'), ('force1d', 'forces1d'),
                        ('force1d_band', '1Dforce_band'), ('torque', 'torques'),
                        ('torque1d', '1Dtorques'), ('torque1d_band', 'torque1d_bands'),
                        ('time', 'times'), ('time_band', 'time_bands'),
                        ('text', 'texts'), ('mass', 'mass')]

        processors = [self.customProcessor(
            i[0], mdxDataItem, required=False) for i in tags_aliases]
        processors_arrays = [xml.array(pr, alias='_' + name[1])
                             for pr, name in zip(processors, tags_aliases)]

        # processors_arrays += [xml.string('text', alias='_text')]

        stream_processor = xml.user_object('stream', mdxStream, [
            xml.string('.', attribute='frequency', alias='_frequency'),
            xml.string('.', attribute='description',
                       alias='_description', required=False),
            xml.string('.', attribute='label', alias='_label', required=False),
            xml.integer('.', attribute='nFrames', alias='_nFrames'),
            xml.integer('.', attribute='startTime', alias='_startTime')] + processors_arrays, alias='_streams', required=False
        )

        static_processor = xml.user_object('static', mdxStatic, [
            xml.string('.', attribute='description',
                       alias='_description', required=False),
            xml.string('.', attribute='label', alias='_label', required=False)
        ] + processors_arrays, alias='_static')

        cycle_processor = xml.user_object('cycle', mdxCycle, [
            xml.string('.', attribute='description',
                       alias='_description', required=False),
            xml.string('.', attribute='label', alias='_label', required=False)
        ] + processors_arrays, required=False)

        corner1_processor = xml.dictionary('corner1', [
            xml.floating_point('.', attribute='x', alias='_x'),
            xml.floating_point('.', attribute='y', alias='_y'),
            xml.floating_point('.', attribute='z', alias='_z')], alias='_corner1')

        corner2_processor = xml.dictionary('corner2', [
            xml.floating_point('.', attribute='x', alias='_x'),
            xml.floating_point('.', attribute='y', alias='_y'),
            xml.floating_point('.', attribute='z', alias='_z')], alias='_corner2')

        corner3_processor = xml.dictionary('corner3', [
            xml.floating_point('.', attribute='x', alias='_x'),
            xml.floating_point('.', attribute='y', alias='_y'),
            xml.floating_point('.', attribute='z', alias='_z')], alias='_corner3')

        corner4_processor = xml.dictionary('corner4', [
            xml.floating_point('.', attribute='x', alias='_x'),
            xml.floating_point('.', attribute='y', alias='_y'),
            xml.floating_point('.', attribute='z', alias='_z')], alias='_corner4')

        platform_processor = xml.dictionary('platform', [
            xml.string('.', attribute='label', alias='_label'),
            corner1_processor,
            corner2_processor,
            corner3_processor,
            corner4_processor])

        volume_processor = xml.dictionary('volume', [
            xml.floating_point('.', attribute='xMax', alias='_xMax'),
            xml.floating_point('.', attribute='xMin', alias='_xMin'),
            xml.floating_point('.', attribute='yMax', alias='_yMax'),
            xml.floating_point('.', attribute='yMin', alias='_yMin'),
            xml.floating_point('.', attribute='zMax', alias='_zMax'),
            xml.floating_point('.', attribute='zMin', alias='_zMin'),
        ], alias='_volume')

        platforms_processor = xml.dictionary('platforms', [
            xml.integer('.', attribute='nPlats', alias='_nPlats'),
            xml.array(platform_processor, alias='_platforms'),
        ], alias='_platforms')

        calibration_processor = xml.dictionary('calibration', [
            platforms_processor, volume_processor
        ], alias='_calibration', required=False)

        link_processor = xml.dictionary('link', [
            xml.string('.', attribute='label1', alias='_label1'),
            xml.string('.', attribute='label2', alias='_label2')], alias='_link')

        stick_model_processor = xml.dictionary('stick_model', [
            xml.array(link_processor, alias='_links'),
            xml.string('.', attribute='label', alias='_label'),
            xml.integer('.', attribute='nLinks', alias='_nLinks')], alias='_stick_model', required=False)

        trial_processor = xml.user_object('trial', mdxTrial, [
            xml.string('.', attribute='date', alias='_date'),
            xml.string('.', attribute='description',
                       alias='_description', required=False),
            xml.string('.', attribute='label', alias='_label'),
            xml.string('.', attribute='time', alias='_time', required=False),
            xml.array(stream_processor, alias='streams'),
            static_processor, cycle_processor, calibration_processor, stick_model_processor], alias='trial')

        self.mdx_processor = xml.dictionary("emxDataFile", [trial_processor,
                                                            xml.floating_point(
                                                                '.', attribute='format', alias='_format'),
                                                            xml.string('.', attribute='sourceApp', alias='_sourceApp')])

        self.dat = xml.parse_from_file(self.mdx_processor, self.filename)
        self.trial = self.dat['trial']

    def write(self, filename, value):
        xml.serialize_to_file(root_processor=self.mdx_processor,
                              xml_file_path=filename,
                              value=value, indent="\t")

    def update(self):
        self.write(self.filename, self.dat)


def main():
    a = mdxParser('../tests/test_files/2255~aa~Walking 01.mdx')
    print(a.trial.markerStream.toTRC(filename='test.trc', trim=True))


if __name__ == '__main__':
    main()
