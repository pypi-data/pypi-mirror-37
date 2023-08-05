# coding: utf-8
from __future__ import unicode_literals

import base64
import numpy as np
import os
import platform
import sys
import unittest
import zlib

from contextlib import contextmanager
from ctypes import *
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock, PropertyMock

import tecplot as tp
from tecplot import session
from tecplot.constant import *
from tecplot.exception import *

from test import patch_tecutil, skip_if_sdk_version_before

from ..sample_data import sample_data_file

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.filenames = [
            sample_data_file('10x10x10'),
            sample_data_file('3x3_2x2')]

    def tearDown(self):
        tp.new_layout()
        for f in self.filenames:
            os.remove(f)

    def test_extract_default_args(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(.5,.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, multiple_zones=False,
            copy_cell_centers=False, assign_strand_ids=False, frame=None,
            dataset=None)

        self.assertIsInstance(z, tp.data.ClassicFEZone)

    def test_extract_nondefault_args(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(.5,.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, multiple_zones=True,
            copy_cell_centers=True, assign_strand_ids=True, frame=fr,
            dataset=None)

        self.assertIsInstance(z, list)
        self.assertEqual(len(z), 1)

    def test_dataset_frame_mismatch(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        newfr = tp.active_page().add_frame()
        newfr.create_dataset('D', ['x','y'])

        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_slice(dataset=ds, frame=newfr)

    @skip_if_sdk_version_before(2017, 3)
    def test_interpolate_linear(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(0.5,0.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, dataset=ds)
        self.assertIn(z, ds)
        self.assertEqual(z.name, 'Slice: Y=0.5')

    def test_interpolate_linear_failures(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        with patch_tecutil('CreateSliceZoneFromPlneX', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            tp.data.extract.extract_slice((0.5,0.5,100), (0,0,1))

        if __debug__:
            tp.new_layout()
            ds = tp.data.load_tecplot(self.filenames[1])

            fr = tp.active_frame()
            fr.plot_type = PlotType.Cartesian2D
            with self.assertRaises(TecplotLogicError):
                tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[1])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D
        with self.assertRaises(TecplotLogicError):
            tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

    def test_extract_line_3d(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1., 1., 1.)]
        z = tp.data.extract.extract_line(pts)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1., 1., 1.)]
        z = tp.data.extract.extract_line(pts, num_points=10)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (10,))

        def pts():
            for p in ((.5, .5, .5), (.8, .8, .8), (1., 1., 1.)):
                yield p
        z = tp.data.extract.extract_line(pts())
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1.1, 1.1, 1.1)]
        z = tp.data.extract.extract_line(pts)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (2,))

        pts = [(1.1, 1.1, 1.1)]
        nzones = ds.num_zones
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_line(pts)
        self.assertEqual(nzones, ds.num_zones)

    def test_extract_line_2d(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian2D
        fr.plot().fieldmap(0).surfaces.surfaces_to_plot = SurfacesToPlot.KPlanes

        pts = [
            (.5, .5),
            (.8, .8),
            (1., 1.)]
        z = tp.data.extract.extract_line(pts, frame=fr)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5),
            (.8, .8),
            (1.1, 1.1)]
        z = tp.data.extract.extract_line(pts, dataset=ds)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (2,))

        pts = [(1.1, 1.1)]
        nzones = ds.num_zones
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_line(pts, frame=fr, dataset=ds)
        self.assertEqual(nzones, ds.num_zones)

    def test_extract_line_failures(self):
        if __debug__:
            tp.new_layout()
            ds = tp.data.load_tecplot(self.filenames[0])
            fr = tp.active_frame()

            pts = [
                (.5, .5, .5),
                (.8, .8, .8),
                (1., 1., 1.)]

            fr.plot_type = PlotType.Sketch

            with self.assertRaises(TecplotLogicError):
                z = tp.data.extract.extract_line(pts)

            fr.plot_type = PlotType.Cartesian3D
            fr2 = tp.active_page().add_frame()
            ds2 = tp.data.load_tecplot(self.filenames[0])
            with self.assertRaises(TecplotLogicError):
                z = tp.data.extract.extract_line(pts, frame=fr, dataset=ds2)


if __name__ == '__main__':
    from .. import main
    main()
