#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `simplemdxparser` package."""

import os
from datetime import date, time

import pytest
from click.testing import CliRunner
from past.builtins import basestring

from simplemdx import cli
from simplemdx.declparser import mdxCycle, mdxParser, mdxStream, mdxTrial, mdxItem, coordToSegments, segmentsToCoord
from simplemdx.parser import MarkerStream, Parser, Segment, emgStream

test_files_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files')


"""
class TestParser(object):
    \"\"\"pytest class for the parser\"\"\"

    def trialMDX(self):
        return Parser(os.path.join(test_files_dir, u'1477~ac~Walking 01.mdx'))

    def sessionMDX(self):
        return Parser(os.path.join(test_files_dir, u'2148~aa~Descalzo con bastón.mdx'))

    def test_parse_trialMDX(self):
        a = self.trialMDX()
        assert a.format == '0.1'
        assert a.sourceApp == 'Viper'

        assert a.trial
        assert not a.norm
        assert a.date == date(2000, 1, 1)
        assert a.time == time(0, 0, 0)
        assert a.label == '1477~ac~Walking 01.tdf'
        assert a.description == "SMART acquisition"

    def test_trial_markers(self):
        a = self.trialMDX()
        assert isinstance(a.markers, MarkerStream)
        assert len(a.markers) == 53 == len(a.markers.items)
        assert len(a.markers.references) == 16

        c7 = a.markers['c7']
        assert c7 == a.markers[0]
        assert c7.name == 'track'
        assert isinstance(c7.label, basestring)
        assert c7.nSegs == len(c7.data) == 2
        assert c7.nPoints == sum(len(i) for i in c7.data) == 532

        dc = c7.datac
        assert isinstance(dc, Segment)
        # The length in continuous mode of any marker shoud be the
        # the same as the stream's frame number
        assert len(dc.X) == a.markers.nFrames
        assert len(dc.Y) == a.markers.nFrames
        assert len(dc.Z) == a.markers.nFrames

    def test_trial_emg(self):
        a = self.trialMDX()
        assert isinstance(a.emg, emgStream)
        assert a.emg[0] == a.emg['Left Rectus femoris']
        assert isinstance(a.emg[0].data, Segment)
        assert a.emg[0].data.frame == 0
        assert len(a.emg[0].data.V) == 10253

        # If single segment, data == datac
        assert a.emg[0].data.V == a.emg[0].datac.V

    def test_trial_events(self):
        a = self.trialMDX()
        assert a.static['eLHS'].data == [3.81, 4.73]
        assert a.static['eLTO'].data == 4.36
        assert a.static['eRTO'].data == 4.83

    def test_parseSessionMDX(self):
        a = self.sessionMDX()
        b = a.session
        assert b.name == u'CACHO'
        assert b.lastname == u'CASTAÑA'
        assert b.birthday == date(1959, 12, 1)
        assert b.date == date(2017, 7, 4)
        assert b.age == 57

        assert b.sex == 'M'
        assert b.clinician == "Who, Doctor"
        assert b.taxid == 'TEC'

        assert b.address == ", ,  "

        assert b.mass == b['mTB'].data == 79.0
        assert b.height == b['dTH'].data == 1.74

        assert b.right_leg_length == b['dRLL'].data == 0.94
        assert b.left_leg_length == b['dLLL'].data == 0.93

        assert b.right_pelvis_depth == b['dRPD'].data == 0.11
        assert b.left_pelvis_depth == b['dLPD'].data == 0.11

        assert b.asis_breadth == b['dAB'].data == 0.25

    def test_Segment(self):
        # a = Segment()
        pass
"""


@pytest.fixture
def d():

    return {
        'data': 'S 0 1 2 3 4 5 6 77 88 99 10',
        'coord': 'X',
        'coords': ['X'],
        'scaleFactor': 1,
        'nFrames': None,
        'result': [1, 2, 3, 4, 5, 6, 77, 88, 99, 10]
    }


class TestSerializing(object):
    """pytest class for the deserializing function"""

    def test_segmentsToCoord(self, d):

        assert segmentsToCoord(d['data'], d[
                               'coord'], d['coords'], d['scaleFactor'], d['nFrames']) == d['result']

    def test_coords(self, d):
        coord = 'Xn'

        with pytest.raises(ValueError):
            assert segmentsToCoord(
                d['data'], coord, d['coords'], d['scaleFactor'], d['nFrames'])

        coord = 'Y'
        coords = ['X', 'Y']

        assert segmentsToCoord(
            d['data'], coord, coords, d['scaleFactor'], d['nFrames']) == [2, 4, 6, 88, 10]

        coord = 'X'
        

    def test_nFrames(self, d):
        nFrames = 15
        res = segmentsToCoord(
            d['data'], d['coord'], d['coords'], d['scaleFactor'], nFrames)

        assert res == d['result'] + [None] * 5


class TestDeclarativeParser(object):
    """pytest class for the declarative parser"""

    def trialMDX(self):
        return mdxParser(os.path.join(test_files_dir, u'1477~ac~Walking 01.mdx'))

    def sessionMDX(self):
        return mdxParser(os.path.join(test_files_dir, u'2148~aa~Descalzo con bastón.mdx'))

    def test_parse_trialMDX(self):
        a = self.trialMDX()

        assert a.trial
        t = a.trial

        assert t._date == '31-12-2000'
        assert t.date == date(year=2000, month=12, day=31)

        t.date = date(year=2000, month=10, day=11)
        assert t._date == '11-10-2000'
        assert t.date == date(year=2000, month=10, day=11)

        assert t._time == '12:58:45'
        assert t.time == time(hour=12, minute=58, second=45)

        t.time = time(hour=5, minute=12, second=45)
        assert t._time == '05:12:45'
        assert t.time == time(hour=5, minute=12, second=45)

        assert t.label == '1477~ac~Walking 01.tdf'
        t.label = 'ññásdfásd´fásd´g´´asdfasdfffff'
        assert t.label == 'ññásdfásd´fásd´g´´asdfasdfffff'

        assert t.description == "SMART acquisition"
        t.description = 'ññásdfásd´fásd´g´´asdfasdfffff'
        assert t.description == 'ññásdfásd´fásd´g´´asdfasdfffff'

    def test_mdxItem(self):
        item = mdxItem()


    def test_parse_stream(self):
        a = self.trialMDX().trial.streams
        assert isinstance(a, list)

    @pytest.mark.skip
    def test_trial_markers(self):
        a = self.trialMDX().trial
        assert isinstance(a.markerStream, mdxStream)
        assert len(a.markers) == 53 == len(a.markers.items)
        assert len(a.markers.references) == 16

        c7 = a.markers['c7']
        assert c7 == a.markers[0]
        assert c7.name == 'track'
        assert isinstance(c7.label, basestring)
        assert c7.nSegs == len(c7.data) == 2
        assert c7.nPoints == sum(len(i) for i in c7.data) == 532

        dc = c7.datac
        assert isinstance(dc, Segment)
        # The length in continuous mode of any marker shoud be the
        # the same as the stream's frame number
        assert len(dc.X) == a.markers.nFrames
        assert len(dc.Y) == a.markers.nFrames
        assert len(dc.Z) == a.markers.nFrames

    @pytest.mark.skip
    def test_trial_emg(self):
        a = self.trialMDX()
        assert isinstance(a.emg, emgStream)
        assert a.emg[0] == a.emg['Left Rectus femoris']
        assert isinstance(a.emg[0].data, Segment)
        assert a.emg[0].data.frame == 0
        assert len(a.emg[0].data.V) == 10253

        # If single segment, data == datac
        assert a.emg[0].data.V == a.emg[0].datac.V

    @pytest.mark.skip
    def test_trial_events(self):
        a = self.trialMDX()
        assert a.static['eLHS'].data == [3.81, 4.73]
        assert a.static['eLTO'].data == 4.36
        assert a.static['eRTO'].data == 4.83

    @pytest.mark.skip
    def test_parseSessionMDX(self):
        a = self.sessionMDX()
        b = a.session
        assert b.name == u'CACHO'
        assert b.lastname == u'CASTAÑA'
        assert b.birthday == date(1959, 12, 1)
        assert b.date == date(2017, 7, 4)
        assert b.age == 57

        assert b.sex == 'M'
        assert b.clinician == "Who, Doctor"
        assert b.taxid == 'TEC'

        assert b.address == ", ,  "

        assert b.mass == b['mTB'].data == 79.0
        assert b.height == b['dTH'].data == 1.74

        assert b.right_leg_length == b['dRLL'].data == 0.94
        assert b.left_leg_length == b['dLLL'].data == 0.93

        assert b.right_pelvis_depth == b['dRPD'].data == 0.11
        assert b.left_pelvis_depth == b['dLPD'].data == 0.11

        assert b.asis_breadth == b['dAB'].data == 0.25

    @pytest.mark.skip
    def test_Segment(self):
        # a = Segment()
        pass


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'simplemdx.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
