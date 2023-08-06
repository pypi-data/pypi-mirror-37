# Copyright 2018 CITS3200 2018 Group C, University of Western Australia
# Copyright (c) 2016 Bioinformatics Laboratory, University of Ljubljana,
#   Faculty of Computer and Information Science
#
# This file is part of Geo.
#
#    Geo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Geo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Geo.  If not, see <https://www.gnu.org/licenses/>.

import os
from itertools import chain, repeat
from collections import OrderedDict
from tempfile import mkstemp

import numpy as np

from AnyQt.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot, QTimer, QT_VERSION, QObject, QDate, QDateTime
from AnyQt.QtGui import QImage, QPainter, QPen, QBrush, QColor, \
                        QMainWindow, QMenuBar, QMenu, QIntValidator, QDoubleValidator, \
                        QMessageBox, QPixmap
from AnyQt.QtWidgets import qApp, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QLineEdit


from Orange.util import color_to_hex
from Orange.base import Learner
from Orange.data.util import scale
from Orange.data import Table, Domain, TimeVariable, DiscreteVariable, ContinuousVariable
from Orange.widgets import gui, widget, settings
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.utils.webview import WebviewWidget
from Orange.widgets.utils.colorpalette import ColorPaletteGenerator, ContinuousPaletteGenerator
from Orange.widgets.utils.annotated_data import create_annotated_table, ANNOTATED_DATA_SIGNAL_NAME
from Orange.widgets.widget import Input, Output, OWWidget

# Edited by Thomas
from Orange.widgets.data import owtable
from AnyQt.QtWidgets import QDockWidget
from Orange.widgets.utils.itemmodels import TableModel
# End Thomas

from orangecontrib.geof.utils import find_lat_lon
from orangecontrib.geof.HRangeSlider import HRangeSlider


if QT_VERSION <= 0x050300:
    raise RuntimeError('Map widget only works with Qt 5.3+')


class LeafletMap(WebviewWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, parent=None):

        class Bridge(QObject):
            @pyqtSlot()
            def fit_to_bounds(_):
                return self.fit_to_bounds()

            @pyqtSlot(float, float, float, float)
            def selected_area(_, *args):
                return self.selected_area(*args)

            @pyqtSlot('QVariantList')
            def recompute_heatmap(_, *args):
                return self.recompute_heatmap(*args)

            @pyqtSlot(float, float, float, float, int, int, float, 'QVariantList', 'QVariantList')
            def redraw_markers_overlay_image(_, *args):
                return self.redraw_markers_overlay_image(*args)

            @pyqtSlot(int)
            def selected_marker(_, *args):
                return self.selected_marker(*args)

            @pyqtSlot('QVariantList')
            def calculateGrids(_, *args):
                return self._owwidget._calculateGrids(*args)

            @pyqtSlot()
            def redrawWeather(_):
                if self._owwidget.weatherGenerateAll:
                    return self._owwidget.clearGrids()
                else:
                    return self._owwidget.generateGrids()

        super().__init__(parent,
                         bridge=Bridge(),
                         url=QUrl(self.toFileURL(
                             os.path.join(os.path.dirname(__file__), '_leaflet', 'owmap.html'))),
                         debug=True,)
        self.jittering = 0
        self._jittering_offsets = None
        self._owwidget = parent
        self._opacity = 255
        self._sizes = None
        self._selected_indices = None

        self.lat_attr = None
        self.lon_attr = None
        self.data = None
        self.model = None
        self._domain = None
        self._latlon_data = None

        self._jittering = None
        self._color_attr = None
        self._label_attr = None
        self._shape_attr = None
        self._size_attr = None
        self._legend_colors = []
        self._legend_shapes = []
        self._legend_sizes = []

        self._drawing_args = None
        self._image_token = None
        self._prev_map_pane_pos = None
        self._prev_origin = None
        self._overlay_image_path = mkstemp(prefix='orange-Map-', suffix='.png')[1]
        self._subset_ids = np.array([])
        self.is_js_path = None

        self._should_fit_bounds = False

        # Time data variables
        self.timeAttr = None   # Name of the data time attribute
        self.timeLower = None  # Lower bound on time filter
        self.timeUpper = None  # Upper bound on time filter

        self._timeData = None
    
    # Setter function for time attribute data
    def setTimeData(self, timedata):
        self._timeData = timedata

    # Setter function for time bounds
    def setTimeBounds(self, lower, upper):
        self.timeLower = lower
        self.timeUpper = upper
        self.redraw_markers_overlay_image()

    def __del__(self):
        os.remove(self._overlay_image_path)
        self._image_token = np.nan

    def set_data(self, data, lat_attr, lon_attr, update=False):
        self.data = data
        self._image_token = np.nan  # Stop drawing previous image
        self._owwidget.progressBarFinished(None)
        self._owwidget.Warning.all_nan_slice.clear()

        if (data is None or not len(data) or
                lat_attr not in data.domain or
                lon_attr not in data.domain):
            self.data = None
            self.evalJS('clear_markers_js(); clear_markers_overlay_image();')
            self._legend_colors = []
            self._legend_shapes = []
            self._legend_sizes = []
            self._update_legend()
            return

        lat_attr = data.domain[lat_attr]
        lon_attr = data.domain[lon_attr]

        fit_bounds = (self._domain != data.domain or
                      self.lat_attr is not lat_attr or
                      self.lon_attr is not lon_attr)
        self.lat_attr = lat_attr
        self.lon_attr = lon_attr
        self._domain = data.domain

        self._latlon_data = np.array([
            self.data.get_column_view(self.lat_attr)[0],
            self.data.get_column_view(self.lon_attr)[0]],
            dtype=float, order='F').T

        self._recompute_jittering_offsets()

        # Lat and/or Long is all-NaN. Clear the image and warn.
        if np.isnan(self._latlon_data).all(axis=0).any():
            self._owwidget.Warning.all_nan_slice()
            self.redraw_markers_overlay_image(new_image=True)
            return

        if fit_bounds:
            if self.isVisible():
                QTimer.singleShot(1, self.fit_to_bounds)
            else:
                self._should_fit_bounds = True
        elif update:
            self.redraw_markers_overlay_image(new_image=True)

    def showEvent(self, event):
        super().showEvent(event)
        if self._should_fit_bounds:
            QTimer.singleShot(500, self.fit_to_bounds)
            self._should_fit_bounds = False

    def fit_to_bounds(self, fly=True):
        if self.data is None:
            return
        lat_data, lon_data = self._latlon_data.T
        if np.isnan(lat_data).all() or np.isnan(lon_data).all():
            script = 'map.setView([0, 0], 0)'
        else:
            north, south = np.nanmax(lat_data), np.nanmin(lat_data)
            east, west = np.nanmin(lon_data), np.nanmax(lon_data)
            script = ('map.%sBounds([[%f, %f], [%f, %f]], {padding: [0,0], minZoom: 2, maxZoom: 13})' %
                      ('flyTo' if fly else 'fit', south, west, north, east))
        self.evalJS(script)
        # Sometimes on first data, it doesn't zoom in enough. So let do it
        # once more for good measure!
        self.evalJS(script)

    def selected_marker(self, id):
        indices = None
        id = self._visible[id]
        prev_selected_indices = self._selected_indices
        if self.data is not None:
            indices = np.full(self._latlon_data.T[0].size, False)
            indices[id] = True
            if self._selected_indices is not None:
                indices |= self._selected_indices
            self._selected_indices = indices
        else:
            self._selected_indices = None
        if np.any(self._selected_indices != prev_selected_indices):
            self.selectionChanged.emit(indices.nonzero()[0].tolist())
            self.redraw_markers_overlay_image(new_image=True)

    def selected_area(self, north, east, south, west):
        indices = np.array([])
        prev_selected_indices = self._selected_indices
        if self.data is not None and (north != south and east != west):
            lat, lon = self._latlon_data.T
            indices = ((lat <= north) & (lat >= south) &
                        (lon <= east) & (lon >= west))
            # add time bounds to comparison
            tm = self._timeData
            t1 = self.timeLower
            t2 = self.timeUpper

            if tm is not None and t1 is not None:
                indices = ((indices) &
                            (tm <= t2) & (tm >= t1))


            if self._selected_indices is not None:
                indices |= self._selected_indices
            self._selected_indices = indices
        else:
            self._selected_indices = None
        if np.any(self._selected_indices != prev_selected_indices):
            self.selectionChanged.emit(indices.nonzero()[0].tolist())
            self.redraw_markers_overlay_image(new_image=True)

    def set_map_provider(self, provider):
        self.evalJS('set_map_provider("{}");'.format(provider))

    def set_clustering(self, cluster_points):
        self.evalJS('''
            window.cluster_points = {};
            set_cluster_points();
        '''.format(int(cluster_points)))

    def _recompute_jittering_offsets(self):
        if not self._jittering:
            self._jittering_offsets = None
        elif self.data:
            # Calculate offsets randomly distributed within a circle
            screen_size = max(100, min(qApp.desktop().screenGeometry().width(),
                                       qApp.desktop().screenGeometry().height()))
            n = len(self.data)
            r = np.random.random(n)
            theta = np.random.uniform(0, 2*np.pi, n)
            xy_offsets = screen_size * self._jittering * np.c_[r * np.cos(theta),
                                                               r * np.sin(theta)]
            self._jittering_offsets = xy_offsets

    def set_jittering(self, jittering):
        """ In percent, i.e. jittering=3 means 3% of screen height and width """
        self._jittering = jittering / 100
        self._recompute_jittering_offsets()
        self.redraw_markers_overlay_image(new_image=True)

    @staticmethod
    def _legend_values(variable, values):
        strs = [variable.repr_val(val) for val in values]
        if any(len(val) > 10 for val in strs):
            if isinstance(variable, TimeVariable):
                strs = [s.replace(' ', '<br>') for s in strs]
            elif variable.is_continuous:
                strs = ['{:.4e}'.format(val) for val in values]
            elif variable.is_discrete:
                strs = [s if len(s) <= 12 else (s[:8] + '…' + s[-3:])
                        for s in strs]
        return strs

    def set_marker_color(self, attr, update=True):
        try:
            self._color_attr = variable = self.data.domain[attr]
            if len(self.data) == 0:
                raise Exception
        except Exception:
            self._color_attr = None
            self._legend_colors = []
        else:
            if variable.is_continuous:
                self._raw_color_values = values = self.data.get_column_view(variable)[0].astype(float)
                self._scaled_color_values = scale(values)
                self._colorgen = ContinuousPaletteGenerator(*variable.colors)

                colors = [color_to_hex(i) for i in variable.colors[:2]]
                if variable.colors[2]:  # pass through black
                    colors.insert(1, 'black')

                min = np.nanmin(values)
                self._legend_colors = (
                    ['c', self._legend_values(variable, [min, np.nanmax(values)]), colors]
                    if not np.isnan(min) else [])
            elif variable.is_discrete:
                _values = np.asarray(self.data.domain[attr].values)
                __values = self.data.get_column_view(variable)[0].astype(np.uint16)
                self._raw_color_values = _values[__values]  # The joke's on you
                self._scaled_color_values = __values
                self._colorgen = ColorPaletteGenerator(len(variable.colors), variable.colors)
                self._legend_colors = ['d',
                                       self._legend_values(variable, range(len(_values))),
                                       list(_values),
                                       [color_to_hex(self._colorgen.getRGB(i))
                                        for i in range(len(_values))]]
        finally:
            if update:
                self.redraw_markers_overlay_image(new_image=True)

    def set_marker_label(self, attr, update=True):
        try:
            self._label_attr = variable = self.data.domain[attr]
            if len(self.data) == 0:
                raise Exception
        except Exception:
            self._label_attr = None
        else:
            if variable.is_continuous or variable.is_string:
                self._label_values = self.data.get_column_view(variable)[0]
            elif variable.is_discrete:
                _values = np.asarray(self.data.domain[attr].values)
                __values = self.data.get_column_view(variable)[0].astype(np.uint16)
                self._label_values = _values[__values]  # The design had lead to poor code for ages
        finally:
            if update:
                self.redraw_markers_overlay_image(new_image=True)

    def set_marker_shape(self, attr, update=True):
        try:
            self._shape_attr = variable = self.data.domain[attr]
            if len(self.data) == 0:
                raise Exception
        except Exception:
            self._shape_attr = None
            self._legend_shapes = []
        else:
            assert variable.is_discrete
            _values = np.asarray(self.data.domain[attr].values)
            self._shape_values = __values = self.data.get_column_view(variable)[0].astype(np.uint16)
            self._raw_shape_values = _values[__values]
            self._legend_shapes = [self._legend_values(variable, range(len(_values))),
                                   list(_values)]
        finally:
            if update:
                self.redraw_markers_overlay_image(new_image=True)

    def set_marker_size(self, attr, update=True):
        try:
            self._size_attr = variable = self.data.domain[attr]
            if len(self.data) == 0:
                raise Exception
        except Exception:
            self._size_attr = None
            self._legend_sizes = []
        else:
            assert variable.is_continuous
            self._raw_sizes = values = self.data.get_column_view(variable)[0].astype(float)
            # Note, [5, 60] is also hardcoded in legend-size-indicator.svg
            self._sizes = scale(values, 5, 60).astype(np.uint8)
            min = np.nanmin(values)
            self._legend_sizes = self._legend_values(variable,
                                                     [min, np.nanmax(values)]) if not np.isnan(min) else []
        finally:
            if update:
                self.redraw_markers_overlay_image(new_image=True)

    def set_marker_size_coefficient(self, size):
        self._size_coef = size / 100
        self.evalJS('''set_marker_size_coefficient({});'''.format(size / 100))
        if not self.is_js_path:
            self.redraw_markers_overlay_image(new_image=True)

    def set_marker_opacity(self, opacity):
        self._opacity = 255 * opacity // 100
        self.evalJS('''set_marker_opacity({});'''.format(opacity / 100))
        if not self.is_js_path:
            self.redraw_markers_overlay_image(new_image=True)

    def set_model(self, model):
        self.model = model
        self.evalJS('clear_heatmap()' if model is None else 'reset_heatmap()')

    def recompute_heatmap(self, points):
        if self.model is None or self.data is None:
            self.exposeObject('model_predictions', {})
            self.evalJS('draw_heatmap()')
            return

        latlons = np.array(points)
        table = Table(Domain([self.lat_attr, self.lon_attr]), latlons)
        try:
            predictions = self.model(table)
        except Exception as e:
            self._owwidget.Error.model_error(e)
            return
        else:
            self._owwidget.Error.model_error.clear()

        class_var = self.model.domain.class_var
        is_regression = class_var.is_continuous
        if is_regression:
            predictions = scale(np.round(predictions, 7))  # Avoid small errors
            kwargs = dict(
                extrema=self._legend_values(class_var, [np.nanmin(predictions),
                                                        np.nanmax(predictions)]))
        else:
            colorgen = ColorPaletteGenerator(len(class_var.values), class_var.colors)
            predictions = colorgen.getRGB(predictions)
            kwargs = dict(
                legend_labels=self._legend_values(class_var, range(len(class_var.values))),
                full_labels=list(class_var.values),
                colors=[color_to_hex(colorgen.getRGB(i))
                        for i in range(len(class_var.values))])
        self.exposeObject('model_predictions', dict(data=predictions, **kwargs))
        self.evalJS('draw_heatmap()')

    def _update_legend(self, is_js_path=False):
        self.evalJS('''
            window.legend_colors = %s;
            window.legend_shapes = %s;
            window.legend_sizes  = %s;
            legendControl.remove();
            legendControl.addTo(map);
        ''' % (self._legend_colors,
               self._legend_shapes if is_js_path else [],
               self._legend_sizes))

    def _update_js_markers(self, visible, in_subset):
        self._visible = visible
        latlon = self._latlon_data
        self.exposeObject('latlon_data', dict(data=latlon[visible]))
        self.exposeObject('jittering_offsets',
                          self._jittering_offsets[visible] if self._jittering_offsets is not None else [])
        self.exposeObject('selected_markers', dict(data=(self._selected_indices[visible]
                                                         if self._selected_indices is not None else 0)))
        self.exposeObject('in_subset', in_subset.astype(np.int8))
        if not self._color_attr:
            self.exposeObject('color_attr', dict())
        else:
            colors = [color_to_hex(rgb)
                      for rgb in self._colorgen.getRGB(self._scaled_color_values[visible])]
            self.exposeObject('color_attr',
                              dict(name=str(self._color_attr), values=colors,
                                   raw_values=self._raw_color_values[visible]))
        if not self._label_attr:
            self.exposeObject('label_attr', dict())
        else:
            self.exposeObject('label_attr',
                              dict(name=str(self._label_attr),
                                   values=self._label_values[visible]))
        if not self._shape_attr:
            self.exposeObject('shape_attr', dict())
        else:
            self.exposeObject('shape_attr',
                              dict(name=str(self._shape_attr),
                                   values=self._shape_values[visible],
                                   raw_values=self._raw_shape_values[visible]))
        if not self._size_attr:
            self.exposeObject('size_attr', dict())
        else:
            self.exposeObject('size_attr',
                              dict(name=str(self._size_attr),
                                   values=self._sizes[visible],
                                   raw_values=self._raw_sizes[visible]))
        self.evalJS('''
            window.latlon_data = latlon_data.data;
            window.selected_markers = selected_markers.data;
            add_markers(latlon_data);
        ''')

    class Projection:
        """This should somewhat model Leaflet's Web Mercator (EPSG:3857).

        Reverse-engineered from L.Map.latlngToContainerPoint().
        """
        @staticmethod
        def latlon_to_easting_northing(lat, lon):
            R = 6378137
            MAX_LATITUDE = 85.0511287798
            DEG = np.pi / 180

            lat = np.clip(lat, -MAX_LATITUDE, MAX_LATITUDE)
            sin = np.sin(DEG * lat)
            x = R * DEG * lon
            y = R / 2 * np.log((1 + sin) / (1 - sin))
            return x, y

        @staticmethod
        def easting_northing_to_pixel(x, y, zoom_level, pixel_origin, map_pane_pos):
            R = 6378137
            PROJ_SCALE = .5 / (np.pi * R)

            zoom_scale = 256 * (2 ** zoom_level)
            x = (zoom_scale * (PROJ_SCALE * x + .5)).round() + (map_pane_pos[0] - pixel_origin[0])
            y = (zoom_scale * (-PROJ_SCALE * y + .5)).round() + (map_pane_pos[1] - pixel_origin[1])
            return x, y

    N_POINTS_PER_ITER = 666

    def redraw_markers_overlay_image(self, *args, new_image=False):
        if not args and not self._drawing_args or self.data is None:
            return

        if args:
            self._drawing_args = args
        north, east, south, west, width, height, zoom, origin, map_pane_pos = self._drawing_args

        lat, lon = self._latlon_data.T
        tm = self._timeData
        t1 = self.timeLower
        t2 = self.timeUpper

        if t1 is None or tm is None:
            visible = ((lat <= north) & (lat >= south) &
                   (lon <= east) & (lon >= west)).nonzero()[0]
        else:
            # add time bounds to comparison
            visible = ((lat <= north) & (lat >= south) &
                   (lon <= east) & (lon >= west) &
                   (tm <= t2) & (tm >= t1)).nonzero()[0]


        in_subset = (np.in1d(self.data.ids, self._subset_ids)
                     if self._subset_ids.size else
                     np.tile(True, len(lon)))

        is_js_path = self.is_js_path = len(visible) < self.N_POINTS_PER_ITER

        self._update_legend(is_js_path)

        np.random.shuffle(visible)
        # Sort points in subset to be painted last
        visible = visible[np.lexsort((in_subset[visible],))]

        if is_js_path:
            self.evalJS('clear_markers_overlay_image()')
            self._update_js_markers(visible, in_subset[visible])
            self._owwidget.disable_some_controls(False)
            return

        self.evalJS('clear_markers_js();')
        self._owwidget.disable_some_controls(True)

        selected = (self._selected_indices
                    if self._selected_indices is not None else
                    np.zeros(len(lat), dtype=bool))
        cur = 0

        im = QImage(self._overlay_image_path)
        if im.isNull() or self._prev_origin != origin or new_image:
            im = QImage(width, height, QImage.Format_ARGB32)
            im.fill(Qt.transparent)
        else:
            dx, dy = self._prev_map_pane_pos - map_pane_pos
            im = im.copy(dx, dy, width, height)
        self._prev_map_pane_pos = np.array(map_pane_pos)
        self._prev_origin = origin

        painter = QPainter(im)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.evalJS('clear_markers_overlay_image(); markersImageLayer.setBounds(map.getBounds());0')

        self._image_token = image_token = np.random.random()

        n_iters = np.ceil(len(visible) / self.N_POINTS_PER_ITER)

        def add_points():
            nonlocal cur, image_token
            if image_token != self._image_token:
                return
            batch = visible[cur:cur + self.N_POINTS_PER_ITER]

            batch_lat = lat[batch]
            batch_lon = lon[batch]

            x, y = self.Projection.latlon_to_easting_northing(batch_lat, batch_lon)
            x, y = self.Projection.easting_northing_to_pixel(x, y, zoom, origin, map_pane_pos)

            if self._jittering:
                dx, dy = self._jittering_offsets[batch].T
                x, y = x + dx, y + dy

            colors = (self._colorgen.getRGB(self._scaled_color_values[batch]).tolist()
                      if self._color_attr else
                      repeat((0xff, 0, 0)))
            sizes = self._size_coef * \
                (self._sizes[batch] if self._size_attr else np.tile(10, len(batch)))

            opacity_subset, opacity_rest = self._opacity, int(.8 * self._opacity)
            self._owwidget.progressBarInit(None)
            for x, y, is_selected, size, color, _in_subset in \
                    zip(x, y, selected[batch], sizes, colors, in_subset[batch]):

                pensize2, selpensize2 = (.35, 1.5) if size >= 5 else (.15, .7)
                pensize2 *= self._size_coef
                selpensize2 *= self._size_coef

                size2 = size / 2
                if is_selected:
                    painter.setPen(QPen(QBrush(Qt.green), 2 * selpensize2))
                    painter.drawEllipse(x - size2 - selpensize2,
                                        y - size2 - selpensize2,
                                        size + selpensize2,
                                        size + selpensize2)
                color = QColor(*color)
                if _in_subset:
                    color.setAlpha(opacity_subset)
                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(QBrush(color.darker(180)), 2 * pensize2))
                else:
                    color.setAlpha(opacity_rest)
                    painter.setBrush(Qt.NoBrush)
                    painter.setPen(QPen(QBrush(color.lighter(120)), 2 * pensize2))

                painter.drawEllipse(x - size2 - pensize2,
                                    y - size2 - pensize2,
                                    size + pensize2,
                                    size + pensize2)

            im.save(self._overlay_image_path, 'PNG')
            self.evalJS('markersImageLayer.setUrl("{}#{}"); 0;'
                        .format(self.toFileURL(self._overlay_image_path),
                                np.random.random()))

            cur += self.N_POINTS_PER_ITER
            if cur < len(visible):
                QTimer.singleShot(10, add_points)
                self._owwidget.progressBarAdvance(100 / n_iters, None)
            else:
                self._owwidget.progressBarFinished(None)
                self._image_token = None

        self._owwidget.progressBarFinished(None)
        QTimer.singleShot(10, add_points)

    def set_subset_ids(self, ids):
        self._subset_ids = ids
        self.redraw_markers_overlay_image(new_image=True)

    def toggle_legend(self, visible):
        self.evalJS('''
            $(".legend").{0}();
            window.legend_hidden = "{0}";
        '''.format('show' if visible else 'hide'))


class OWMap(OWWidget):
    name = 'Geo Map'
    description = 'Show data points on a world map.'
    icon = "icons/GeoMap.svg"
    priority = 100


    class Inputs:
        data = Input("Data", Table, default=True)
        weatherData = Input('Weather Data', Table)
        data_subset = Input("Data Subset", Table)
        learner = Input("Learner", Learner)

    class Outputs:
        selected_data = Output("Selected Data", Table, default=True)
        annotated_data = Output(ANNOTATED_DATA_SIGNAL_NAME, Table)

    replaces = [
        "Orange.widgets.visualize.owmap.OWMap",
    ]

    settingsHandler = settings.DomainContextHandler()

    want_main_area = True

    autocommit = settings.Setting(True)
    tile_provider = settings.Setting('Black and white')
    lat_attr = settings.ContextSetting('')
    lon_attr = settings.ContextSetting('')
    class_attr = settings.ContextSetting('(None)')
    color_attr = settings.ContextSetting('')
    label_attr = settings.ContextSetting('')
    shape_attr = settings.ContextSetting('')
    size_attr = settings.ContextSetting('')
    timeAttr = settings.ContextSetting('')
    weatherInterpType = settings.Setting(0)
    weatherSearchDistance = settings.Setting(500)
    weatherInversePower = settings.Setting(2)
    weatherGridSize = settings.Setting(32)
    opacity = settings.Setting(100)
    zoom = settings.Setting(100)
    jittering = settings.Setting(0)
    cluster_points = settings.Setting(False)
    show_legend = settings.Setting(True)
    autocommit = settings.Setting(True)

    _timestamp = settings.ContextSetting('')
    _weatherTimestamp = settings.Setting('')

    TILE_PROVIDERS = OrderedDict((
        ('Black and white', 'OpenStreetMap.BlackAndWhite'),
        ('OpenStreetMap', 'OpenStreetMap.Mapnik'),
        ('Topographic', 'Thunderforest.OpenCycleMap'),
        ('Topographic 2', 'Thunderforest.Outdoors'),
        ('Satellite', 'Esri.WorldImagery'),
        ('Print', 'Stamen.TonerLite'),
        ('Dark', 'CartoDB.DarkMatter'),
        ('Watercolor', 'Stamen.Watercolor'),
    ))

    class Error(widget.OWWidget.Error):
        model_error = widget.Msg("Error predicting: {}")
        learner_error = widget.Msg("Error modelling: {}")

    class Warning(widget.OWWidget.Warning):
        all_nan_slice = widget.Msg('Latitude and/or longitude has no defined values (is all-NaN)')

    UserAdviceMessages = [
        widget.Message(
            'Select markers by holding <b><kbd>Shift</kbd></b> key and dragging '
            'a rectangle around them. Clear the selection by clicking anywhere.',
            'shift-selection')
    ]

    graph_name = "map"


    # IF SEPERATE WINDOW: override showEvent of QDialog to show mainWindow and hide this widget(QDialog)
    def showEvent(self, event):
        #self.mainWindow.show()
        #self._dockControlArea.show()
        #self._dockTimeSlice.show()
        if self.__windowState[0]:
            self._dockControlArea.show()
        if self.__windowState[1]:
            self._dockTimeSlice.show()
        OWWidget.showEvent(self, event)
        # TODO save and store dock widget state
        #OWWidget.hide()
        # QDialog doesnt want to die. Some implementation detail in OWWidget (maybe
        # overridden closeEvent) might be preventing it from closing'''

    def closeEvent(self, event):
        #self.mainWindow.close()
        self.__windowState = (self._dockControlArea.isVisible(), self._dockTimeSlice.isVisible())
        self._dockControlArea.close()
        self._dockTimeSlice.close()
        # TODO save and store dock widget state
        OWWidget.closeEvent(self, event)
        

    def __init__(self):
        super().__init__()
        self.map = map = LeafletMap(self)  # type: LeafletMap
        self.map._widget = self
        self.mainArea.layout().addWidget(map)
        self.selection = None
        self.data = None
        self.learner = None

        self.timeLowerBound = 0
        self.timeUpperBound = 0

        self.weatherData = None
        self._weatherOverlayImagePath = mkstemp(prefix='orange-weatherOverlay-', suffix='.png')[1]

        def selectionChanged(indices):
            self.selection = self.data[indices] if self.data is not None and indices else None
            self._indices = indices
            self.commit()

        map.selectionChanged.connect(selectionChanged)

        def _set_map_provider():
            map.set_map_provider(self.TILE_PROVIDERS[self.tile_provider])

        box = gui.vBox(self.controlArea, 'Map')
        gui.comboBox(box, self, 'tile_provider',
                     orientation=Qt.Horizontal,
                     label='Map:',
                     items=tuple(self.TILE_PROVIDERS.keys()),
                     sendSelectedValue=True,
                     callback=_set_map_provider)

        self._latlon_model = DomainModel(
            parent=self, valid_types=ContinuousVariable)
        self._class_model = DomainModel(
            parent=self, placeholder='(None)', valid_types=DomainModel.PRIMITIVE)
        self._color_model = DomainModel(
            parent=self, placeholder='(Same color)', valid_types=DomainModel.PRIMITIVE)
        self._shape_model = DomainModel(
            parent=self, placeholder='(Same shape)', valid_types=DiscreteVariable)
        self._size_model = DomainModel(
            parent=self, placeholder='(Same size)', valid_types=ContinuousVariable)
        self._label_model = DomainModel(
            parent=self, placeholder='(No labels)')
        self._timeModel = DomainModel(
            parent=self, placeholder='(Not selected)')
        self._weatherModel = DomainModel(
            parent=self, valid_types=ContinuousVariable)
        self._weatherTimeModel = DomainModel(
            parent=self, placeholder='(Not selected)')
        

        def _set_lat_long():
            self.map.set_data(self.data, self.lat_attr, self.lon_attr)
            self.train_model()

        self._combo_lat = combo = gui.comboBox(
            box, self, 'lat_attr', orientation=Qt.Horizontal,
            label='Latitude:', sendSelectedValue=True, callback=_set_lat_long)
        combo.setModel(self._latlon_model)
        self._combo_lon = combo = gui.comboBox(
            box, self, 'lon_attr', orientation=Qt.Horizontal,
            label='Longitude:', sendSelectedValue=True, callback=_set_lat_long)
        combo.setModel(self._latlon_model)

        def _toggle_legend():
            self.map.toggle_legend(self.show_legend)

        gui.checkBox(box, self, 'show_legend', label='Show legend',
                     callback=_toggle_legend)

        box = gui.vBox(self.controlArea, 'Overlay')
        self._combo_class = combo = gui.comboBox(
            box, self, 'class_attr', orientation=Qt.Horizontal,
            label='Target:', sendSelectedValue=True, callback=self.train_model
        )
        self.controls.class_attr.setModel(self._class_model)
        self.set_learner(self.learner)

        box = gui.vBox(self.controlArea, 'Points')
        self._combo_color = combo = gui.comboBox(
            box, self, 'color_attr',
            orientation=Qt.Horizontal,
            label='Color:',
            sendSelectedValue=True,
            callback=lambda: self.map.set_marker_color(self.color_attr))
        combo.setModel(self._color_model)
        self._combo_label = combo = gui.comboBox(
            box, self, 'label_attr',
            orientation=Qt.Horizontal,
            label='Label:',
            sendSelectedValue=True,
            callback=lambda: self.map.set_marker_label(self.label_attr))
        combo.setModel(self._label_model)
        self._combo_shape = combo = gui.comboBox(
            box, self, 'shape_attr',
            orientation=Qt.Horizontal,
            label='Shape:',
            sendSelectedValue=True,
            callback=lambda: self.map.set_marker_shape(self.shape_attr))
        combo.setModel(self._shape_model)
        self._combo_size = combo = gui.comboBox(
            box, self, 'size_attr',
            orientation=Qt.Horizontal,
            label='Size:',
            sendSelectedValue=True,
            callback=lambda: self.map.set_marker_size(self.size_attr))
        combo.setModel(self._size_model)


        def _set_opacity():
            map.set_marker_opacity(self.opacity)

        def _set_zoom():
            map.set_marker_size_coefficient(self.zoom)

        def _set_jittering():
            map.set_jittering(self.jittering)

        def _set_clustering():
            map.set_clustering(self.cluster_points)

        self._opacity_slider = gui.hSlider(
            box, self, 'opacity', None, 1, 100, 5,
            label='Opacity:', labelFormat=' %d%%',
            callback=_set_opacity)
        self._zoom_slider = gui.valueSlider(
            box, self, 'zoom', None, values=(20, 50, 100, 200, 300, 400, 500, 700, 1000),
            label='Symbol size:', labelFormat=' %d%%',
            callback=_set_zoom)
        self._jittering = gui.valueSlider(
            box, self, 'jittering', label='Jittering:', values=(0, .5, 1, 2, 5),
            labelFormat=' %.1f%%', ticks=True,
            callback=_set_jittering)
        self._clustering_check = gui.checkBox(
            box, self, 'cluster_points', label='Cluster points',
            callback=_set_clustering)
        
        # CITS3200: Popup a table of selected data
        
        # - Thomas
        def _export_to_table():
            if self.selection is not None:

                flags = Qt.WindowFlags()
                box = gui.table(self.mainArea)

                dock = QDockWidget("Table", box, flags)

                # Create table out of selected data
                table = owtable.OWDataTable()
                table.set_dataset(self.selection)
                dock.setWidget(table)

                # Pops window out of box
                dock.setFloating(True)

                # Hides the box (how to destroy the box?)
                box.hide()
        

        # Create seperate UI region
        box = gui.vBox(self.controlArea, 'Tabulate Data')
   
        # Create button inside new region
        gui.button(
            box, 
            self, 
            label='View Selected Data in Table', 
            callback=_export_to_table
        )
        # - End Thomas

        gui.rubber(self.controlArea)
        gui.auto_commit(self.controlArea, self, 'autocommit', 'Send Selection')
        
        # CITS3200: time data filter slider

        # Converts timestamp into readable format based on selected
        # timestamp type
        def _timestampToStr(ts):
            if self._combo_timestamp.currentIndex() == 0:
                return str(ts)
            elif self._timeStringFormat is None:
                return QDateTime.fromMSecsSinceEpoch(ts * 1000).toString('yyyy MM dd, hh:mm')
            else:
                return QDateTime.fromMSecsSinceEpoch(ts * 1000).toString(self._timeStringFormat)

        # Callback function for setting the time attribute. Checks that the
        # attribute is in the data before enabling the timebar

        # prevent redraw too often
        self._redrawPending = False
        self._redrawWeatherPending = False
        self._redrawTimer = timer = QTimer(self)
        def _doRedraw():
            if self._redrawPending:
                self.map.setTimeBounds(self.timeLowerBound, self.timeUpperBound)
                self._redrawPending = False
            if self._redrawWeatherPending:
                self._doUpdateWeatherOverlay()
                self._redrawWeatherPending = False
        timer.timeout.connect(_doRedraw)
        timer.start(40) #~25 fps
        

        # Callback function for setting 
        def _setTimeBounds(lower, upper):
            # update map variables
            self.timeLowerBound = lower
            self.timeUpperBound = upper

            if self._lockTimebars:
                tb = self.weatherTimebar
                v0 = tb.valueToSteps(lower - self._timebarLockOffset)
                v1 = v0 + self._timebarLockWeatherStepInterval
                if v0 < 0:
                    tb._setSliderPosition(0, self._timebarLockWeatherStepInterval)
                elif v1 > tb.steps():
                    tb._setSliderPosition(tb.steps() - self._timebarLockWeatherStepInterval, tb.steps())
                else:
                    tb._setSliderPosition(v0, v1)
                
            self._redrawPending = True
            _updateTimebarLabel()
            return

        def _timebarLockMouseReleaseLink(int):
            if self._lockTimebars:
                self.weatherTimebar.updateValues()

        
        # Add the layout for time controls
        self.timeSlice = box = gui.vBox(None)
        box.setContentsMargins(7,7,7,7)

        # converts np array of timedata to UNIX timestamps based on combobox index
        def _timestampsToUNIX(timedata, comboIndex, stringFormat=None):
            processed = np.zeros(timedata.size)
            if (comboIndex == 0):
                for i, t in enumerate(timedata):
                    processed[i] = t
            elif (comboIndex == 1):
                # UNIX Epoch
                for i, t in enumerate(timedata):
                    processed[i] = t
            elif (comboIndex == 2):
                for i, t in enumerate(timedata):
                    # Excel timestamp (1900, Windows)
                    days, fDays = np.modf(t) # split timestamp into days and fraction of day
                    processed[i] = QDateTime(QDate(1900, 1, 1)).addDays(days - 2).addSecs(fDays * 86400).toMSecsSinceEpoch() / 1000
            elif (comboIndex == 3):
                for i, t in enumerate(timedata):
                    # Excel timestamp (1904, MacOS)
                    days, fDays = np.modf(t) # split timestamp into days and fraction of day
                    processed[i] = QDateTime(QDate(1904, 1, 1)).addDays(days - 2).addSecs(fDays * 86400).toMSecsSinceEpoch() / 1000
            elif (comboIndex == 4 and stringFormat is not None):
                for i, t in enumerate(timedata):
                    # Text string
                    processed[i] = QDateTime.fromString(str(t), stringFormat).toMSecsSinceEpoch() / 1000
            else:
                return None

            return processed
        
        def _setTimeAttr():
            if self.data is not None and self.timeAttr in self.data.domain:
                variable = self.data.domain[self.timeAttr]
                if not variable.is_continuous:
                    self._combo_timestamp.setCurrentIndex(4)
                    self._combo_timestamp.setEnabled(False)
                else:
                    self._combo_timestamp.setEnabled(True)

                _setTimeStringFormat()

                timedata = self.data.get_column_view(self.timeAttr)[0]
                processed = _timestampsToUNIX(timedata, self._combo_timestamp.currentIndex(), self._timeStringFormat)
                if processed is None:
                    return
                
                self.timebar.setMaximum(np.nanmax(processed))
                self.timebar.setMinimum(np.nanmin(processed))
                self.timebar.setValue(self.timeLowerBound, self.timeUpperBound)
                self.timebar.setEnabled(True)

                if self.weatherData is not None and self.weatherTimeAttr in self.weatherData.domain:
                    self.weatherTimebar.checkLock.show()

                # update map variables
                self.map.setTimeData(processed)
                self.timebar.setTickList(processed)
            else:
                self.timebar.setEnabled(False)
                self.weatherTimebar.checkLock.hide()
            _updateTimebarLabel()

        # Add time attribute selection combo box
        self._combo_time = combo = gui.comboBox(
            box, self, 'timeAttr',
            orientation=Qt.Horizontal,
            label='Attribute:',
            sendSelectedValue=True,
            callback=_setTimeAttr)
        combo.setModel(self._timeModel)
        combo.activated.connect(_setTimeAttr)

        # Callback function for setting timestamp type
        def _setTimestamp():
            if self._combo_timestamp.currentIndex() == 4:
                self._lineEdit_timeStringFormat.show()
            else:
                self._lineEdit_timeStringFormat.hide()
            _setTimeAttr()

        # Add timestamp format selection combo box
        timestampOptions = ["Raw", "UNIX Timestamp", "Excel Timestamp", "Excel Timestamp (Mac)", "Date/Time Text String"]
        self._combo_timestamp = combo = gui.comboBox(
            box, self, '_timestamp',
            orientation=Qt.Horizontal,
            label='Data type:',
            sendSelectedValue = True,
            items = timestampOptions 
        )
        self._combo_timestamp.currentIndexChanged.connect(_setTimestamp)

        self._timeStringFormat = None

        # Callback function for setting time string format
        def _setTimeStringFormat():
            lineedit = self._lineEdit_timeStringFormat
            newFormat = lineedit.text()
            if QDateTime.fromString(str(self.data.get_column_view(self.timeAttr)[0][0]), newFormat).isValid():
                lineedit.setStyleSheet('color: #000')
                self._timeStringFormat = newFormat
                self.timebar.setEnabled(True)
                _updateTimebarLabel()
            else:
                lineedit.setStyleSheet('color: #f00')
                self._timeStringFormat = None
                self.timebar.setEnabled(False)

        # Time string format for Text timestamp
        self._lineEdit_timeStringFormat = lineedit = QLineEdit(box)
        lineedit.setMaxLength(64)
        lineedit.textChanged.connect(_setTimeStringFormat)
        lineedit.editingFinished.connect(_setTimeAttr)
        lineedit.setPlaceholderText('Text time string format')
        box.layout().addWidget(lineedit)
        box.layout().setAlignment(lineedit, Qt.AlignRight)
        lineedit.hide()

        def _updateTimebarLabel():
            self.timebar.label.setText('%s ~ %s' % (_timestampToStr(self.timeLowerBound),\
             _timestampToStr(self.timeUpperBound)) if self.timebar.isEnabled() else '')

        # Add the timebar
        self.timebar = slider = HRangeSlider()
        slider.setEnabled(False)
        slider.valueChanged.connect(_setTimeBounds)
        slider.sliderReleased.connect(_timebarLockMouseReleaseLink)

        slider.label = gui.widgetLabel(box, '')
        box.layout().addWidget(slider)

        def _toggleTimebarLock():
            # re-set slider ranges
            if self._lockTimebars:
                self.weatherTimebar.updateValues()
                self._timebarLockOffset = self.timebar.value()[0] - self.weatherTimebar.value()[0]
                self._timebarLockWeatherStepInterval = self.weatherTimebar.valueSteps()[1] - self.weatherTimebar.valueSteps()[0]
        
        # weather timebars
        self._lockTimebars = False

        self.weatherTimebar = slider = HRangeSlider()
        gui.separator(box)
        slider.labelName = gui.widgetLabel(box, 'Interpolated overlay')
        slider.labelValue = gui.widgetLabel(box, '')
        box.layout().addWidget(slider)
        slider.checkLock = check = gui.checkBox(
            box, self, '_lockTimebars',
            label='Lock to main slider',
            callback=_toggleTimebarLock
        )
        slider.hide()
        slider.setTracking(False)
        slider.labelName.hide()
        slider.labelValue.hide()
        slider.checkLock.hide()

        gui.rubber(self.timeSlice)

        ## WEATHER WIDGET
        self.weatherTimeData = None

        def _setWeatherAttr():
            _setInterpParams()

        def _setWeatherParamAttr():
            param = self.weatherData.get_column_view(self.weatherParamAttr)[0]
            self.weatherVisualMax = np.nanmax(param)
            self.weatherVisualMin = np.nanmin(param)
            _setInterpParams()

        def _setWeatherTimeAttr():
            if self.weatherData is not None and self.weatherTimeAttr in self.weatherData.domain:
                
                variable = self.weatherData.domain[self.weatherTimeAttr]
                if not variable.is_continuous:
                    self._comboWeatherTimestamp.setCurrentIndex(4)
                    self._comboWeatherTimestamp.setEnabled(False)
                else:
                    self._comboWeatherTimestamp.setEnabled(True)

                timedata = self.weatherData.get_column_view(self.weatherTimeAttr)[0]
                processed = _timestampsToUNIX(timedata, self._comboWeatherTimestamp.currentIndex(), self._weatherTimestringFormat)
                if processed is None:
                    return
                
                self.weatherTimeData = processed

                # for later
                slider = self.weatherTimebar
                slider.show()
                slider.labelValue.show()
                slider.labelName.show()

                # try to match slider step to data granularity
                pmin = np.nanmin(processed)
                pmax = np.nanmax(processed)
                pstep = np.ma.masked_equal(np.diff(np.sort(processed)), 0.0, copy=False).min()
                psteps = (pmax - pmin) / pstep
                slider.setSteps(min(psteps, 1e4))
                slider.setTickList(processed)
                slider.setMinimum(np.nanmin(processed))
                slider.setMaximum(np.nanmax(processed))

                self._lineweatherTimeInterval.setEnabled(True)
                
                if self.data is not None and self.timeAttr in self.data.domain:
                    slider.checkLock.show()
            else:
                self.weatherTimeData = None

                slider = self.weatherTimebar
                slider.hide()
                slider.labelValue.hide()
                slider.labelName.hide()
                slider.checkLock.hide()

                self._lineweatherTimeInterval.setEnabled(False)
            #update label?

        def _setWeatherTimeStringFormat():
            lineedit = self._lineWeatherTimestringFormat
            newFormat = lineedit.text()
            if QDateTime.fromString(str(self.weatherData.get_column_view(self.weatherTimeAttr)[0][0]), newFormat).isValid():
                lineedit.setStyleSheet('color: #000')
                self._weatherTimestringFormat = newFormat
            else:
                lineedit.setStyleSheet('color: #f00')
                self._weatherTimestringFormat = None

        def _setWeatherTimestamp():
            if self._comboWeatherTimestamp.currentIndex() == 4:
                self._lineWeatherTimestringFormat.show()
            else:
                self._lineWeatherTimestringFormat.hide()
            _setWeatherTimeAttr()

        def _weatherTimeBoundsChanged(lower, upper):
            # think about introducing a minimum range for slider
            # or possibly setting a minimum step size but this
            # will do for now
            if not self.weatherGenerateAll:
                self.generateGrids()
            else:
                self._updateWeatherOverlay()

        # signal emitted after valueChanged
        def _weatherTimeIntervalChanged(newInterval):
            self._lineweatherTimeInterval.setText(str(round(newInterval, 7)))
            _setInterpParams()

        self.weatherTimebar.valueChanged.connect(_weatherTimeBoundsChanged)
        self.weatherTimebar.intervalChanged.connect(_weatherTimeIntervalChanged)
        self.weatherTimebar.sliderReleased.connect(_toggleTimebarLock)

        def _setweatherTimeInterval():
            slider = self.weatherTimebar
            slider.setValue(slider.minimum(), slider.minimum() + self.weatherTimeInterval)
            v = slider.value()
        
        def _setInterpParams():
            if self.weatherGenerateAll:
                self.clearGrids()
            else:
                self.generateGrids()

        def _setInterpType():
            return

        def _toggleGenerateAll():
            # show message
            if self.weatherGenerateAll:
                self._buttonGenerateGrids.show()
                self.weatherTimebar.setTracking(True)
                self.clearGrids()
            else:
                self._buttonGenerateGrids.hide()
                self.weatherTimebar.setTracking(False)
                self.generateGrids()

        self.weatherWidget = box = gui.vBox(None)
        box.setContentsMargins(7,7,7,7)

        box = gui.vBox(box, 'Attributes')

        self.weatherLatAttr = ''
        self._comboWeatherLat = combo = gui.comboBox(
            box, self, 'weatherLatAttr',
            orientation=Qt.Horizontal,
            label='Latitude:',
            sendSelectedValue=True,
            callback=_setWeatherAttr)
        combo.setModel(self._weatherModel)
        
        self.weatherLonAttr = ''
        self._comboWeatherLon = combo = gui.comboBox(
            box, self, 'weatherLonAttr',
            orientation=Qt.Horizontal,
            label='Longitude:',
            sendSelectedValue=True,
            callback=_setWeatherAttr)
        combo.setModel(self._weatherModel)

        self.weatherParamAttr = ''
        self._comboWeatherParam = combo = gui.comboBox(
            box, self, 'weatherParamAttr',
            orientation=Qt.Horizontal,
            label='Parameter:',
            sendSelectedValue=True,
            callback=_setWeatherParamAttr)
        combo.setModel(self._weatherModel)

        self.weatherTimeAttr = ''
        self._comboWeatherTime = combo = gui.comboBox(
            box, self, 'weatherTimeAttr',
            orientation=Qt.Horizontal,
            label='Time:',
            sendSelectedValue=True,
            callback=_setWeatherTimeAttr
        )
        combo.setModel(self._weatherTimeModel)
        combo.activated.connect(_setWeatherTimeAttr)

        self._comboWeatherTimestamp = combo = gui.comboBox(
            box, self, '_weatherTimestamp',
            orientation=Qt.Horizontal,
            label='Data type:',
            sendSelectedValue = True,
            items = timestampOptions,
            callback=_setWeatherTimestamp
        )
        combo.currentIndexChanged.connect(_setWeatherTimestamp)

        self._weatherTimestringFormat = None

        self._lineWeatherTimestringFormat = lineedit = QLineEdit(box)
        lineedit.setMaxLength(64)
        lineedit.textChanged.connect(_setWeatherTimeStringFormat)
        lineedit.editingFinished.connect(_setWeatherTimeAttr)
        lineedit.setPlaceholderText('Text time string format')
        box.layout().addWidget(lineedit)
        box.layout().setAlignment(lineedit, Qt.AlignRight)
        lineedit.hide()
        
        box = gui.vBox(self.weatherWidget, 'Interpolation')

        self._radioIntepType = radio = gui.radioButtons(
            box, self, 'weatherInterpType',
            btnLabels=["Inverse Distance Weighting"],
            callback=_setInterpParams)

        qv = QDoubleValidator(box)
        qv.setBottom(0.0)
        self.weatherTimeInterval = None
        self._lineweatherTimeInterval = lineedit = gui.lineEdit(
            box, self, 'weatherTimeInterval',
            label='Average over (days)',
            orientation=Qt.Horizontal,
            validator=qv,
            callback=_setweatherTimeInterval,
            valueType=float)
        lineedit.setEnabled(False)

        self._lineWeatherGridSize = lineedit = gui.lineEdit(
            box, self, 'weatherGridSize',
            label='Grid size:',
            orientation=Qt.Horizontal,
            validator=QIntValidator(1, 4000, box),
            valueType=int,
            callback=_setInterpParams)
        
        self._lineInterpParam1 = lineedit = gui.lineEdit(
            box, self, 'weatherSearchDistance',
            label='Search distance (km):',
            orientation=Qt.Horizontal,
            valueType=int,
            callback=_setInterpParams)

        qv = QDoubleValidator(1e-7, 1e2, 7, box)
        qv.setNotation(QDoubleValidator.StandardNotation)
        self._lineInterpParam2 = lineedit = gui.lineEdit(
            box, self, 'weatherInversePower',
            label='Inverse weighting power, p:',
            validator=qv,
            orientation=Qt.Horizontal,
            valueType=float,
            callback=_setInterpParams
        )

        box = gui.vBox(self.weatherWidget, 'Visualisation')

        self.weatherVisualMin = None
        self._lineVisualMin = lineedit = gui.lineEdit(
            box, self, 'weatherVisualMin',
            label='Min:',
            orientation=Qt.Horizontal,
            valueType=float,
            callback=self._updateWeatherOverlay)

        self.weatherVisualMatchMin = True
        self._checkVisualMatchMin = check = gui.checkBox(
            box, self,
            'weatherVisualMatchMin',
            'Auto'
        )
        
        self.weatherVisualMax = None
        self._lineVisualMax = lineedit = gui.lineEdit(
            box, self, 'weatherVisualMax',
            label='Max:',
            orientation=Qt.Horizontal,
            valueType=float,
            callback=self._updateWeatherOverlay)

        self.weatherVisualMatchMax = True
        self._checkVisualMatchMax = check = gui.checkBox(
            box, self,
            'weatherVisualMatchMax',
            'Auto'
        )

        self.weatherVisualOpacity = 127
        self._sliderVisualOpacity = gui.hSlider(
            box, self, 'weatherVisualOpacity', None, 0, 255, 5,
            label='Opacity:', labelFormat=' %d/255',
            callback=self._updateWeatherOverlay)

        self.weatherGenerateAll = False
        self._checkGenerateAll = check = gui.checkBox(
            self.weatherWidget, self,
            'weatherGenerateAll',
            'Generate all overlays',
            callback=_toggleGenerateAll
        )

        self._buttonGenerateGrids = button = gui.button(
            self.weatherWidget, self,
            label='Generate overlay with current bounds',
            callback=self.generateGrids
        )
        button.hide()

        gui.rubber(self.weatherWidget)

        QTimer.singleShot(0, _set_map_provider)
        QTimer.singleShot(0, _toggle_legend)
        QTimer.singleShot(0, _set_opacity)
        QTimer.singleShot(0, _set_zoom)
        QTimer.singleShot(0, _set_jittering)
        QTimer.singleShot(0, _set_clustering)

        def _showControlArea():
            self._dockControlArea.show()

        def _showTimeSlice():
            self._dockTimeSlice.show()

        def _showDockWeather():
            self._dockWeather.show()

        # QDockWidget can only be used with QMainWindow
        # We have 2 options: create a QMainWindow in the QDialog (OWWidget
        # uses QDialog) or open a seperate QMainWindow and hide/close the
        # QDialog 

        # Currently, we are trying to create a QMainWindow inside QDialog
        # Problems with this approach: ugly margin between window title and menubar
        # Problems with other approach: cant hide/close residual QDialog for some reason

        self.__windowState = (False, False)
        
        self.mainWindow = QMainWindow()
        self.layout().addWidget(self.mainWindow)
        self.layout().setContentsMargins(0,0,0,0)

        #self.controlSplitter.setParent(self.mainWindow)
        self.mainWindow.setCentralWidget(self.mainArea)
        self.mainWindow.setCorner(Qt.BottomLeftCorner, Qt.BottomDockWidgetArea)
        
        # add the control area dock
        self._dockControlArea = dock = QDockWidget('Control Area', self.mainWindow)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setWidget(self.controlArea)
        self.mainWindow.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # add the time slice area dock
        self._dockTimeSlice = dock = QDockWidget('Slice', self.mainWindow)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock.setWidget(self.timeSlice)
        self.mainWindow.addDockWidget(Qt.BottomDockWidgetArea, dock)

        # add the weather dock
        self._dockWeather = dock = QDockWidget('Interpolated overlay', self.mainWindow)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setWidget(self.weatherWidget)
        self.mainWindow.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.hide()

        menubar = self.mainWindow.menuBar()

        menuShowDocks = menubar.addMenu('Show')
        menuShowDocks.addAction('Control area').triggered.connect(_showControlArea)
        menuShowDocks.addAction('Slice').triggered.connect(_showTimeSlice)
        menuShowDocks.addAction('Interpolated overlay').triggered.connect(_showDockWeather)

        menubar.addMenu(menuShowDocks)

        self.weatherGrids = None
    
    def _updateWeatherOverlay(self):
        self._redrawWeatherPending = True

    def _doUpdateWeatherOverlay(self):
        if self.weatherGrids is not None:
            self.map.evalJS('clearWeatherOverlayImage(); weatherLayer.setBounds(map.getBounds());0')
            size = self.weatherGridSize
            image = QImage(size, size, QImage.Format_ARGB32)
            image.fill(QColor.fromHsl(0, 127, 180, self.weatherVisualOpacity))
            if self.weatherGenerateAll:
                grid = self.weatherGrids[self.weatherTimebar.valueSteps()[0]]
            else:
                grid = self.weatherGrids[0]
            if self.weatherVisualMatchMax:
                maxv = np.nanmax(grid)
                self._lineVisualMax.setText(str(maxv))
            else:
                maxv = self.weatherVisualMax
            if self.weatherVisualMatchMin:
                minv = np.nanmin(grid)
                self._lineVisualMin.setText(str(minv))
            else:
                minv = self.weatherVisualMin

            rngv = maxv - minv
            if rngv > 1e-10:
                for i, a in enumerate(grid):
                    image.setPixelColor(i % size, i // size, QColor.fromHsl((a-minv) * 240 // rngv, 127, 180, self.weatherVisualOpacity))
            image.save(self._weatherOverlayImagePath, 'PNG')
            self.map.evalJS('weatherLayer.setUrl("{}#{}"); 0;'
                    .format(self.map.toFileURL(self._weatherOverlayImagePath),
                            np.random.random()))

    def clearGrids(self):
        self.weatherGrids = None
        self.map.evalJS('clearWeatherOverlayImage();')

    
    def generateGrids(self):
        # check that attributes are set
        if self.weatherData is None:
            return
        for attr in (self.weatherLatAttr,
                        self.weatherLonAttr,
                        self.weatherParamAttr,
                        self.weatherTimeAttr):
            if attr is None or attr not in self.weatherData.domain:
                return
        
        # set default parameters?
        # not for now

        # get grid coordinates
        self.map.evalJS('generateCoordGrid(%i)' % self.weatherGridSize)

    def _calculateGrids(self, points):
        # get arrays
        gridlat, gridlon = np.array(points).T
        lat = self.weatherData.get_column_view(self.weatherLatAttr)[0]
        lon = self.weatherData.get_column_view(self.weatherLonAttr)[0]
        param = self.weatherData.get_column_view(self.weatherParamAttr)[0]
        time = np.array(self.weatherTimeData)


        gridsize = int(self.weatherGridSize)

        # get indices of points in range and distances:
        distances = []
        inDistanceRange = []
        for i in range(gridsize * gridsize):
            lat1, lon1, lat2, lon2 = map(np.radians, [gridlat[i], gridlon[i], lat, lon])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
            c = 2 * np.arcsin(np.sqrt(a))
            km = 6367 * c
            distances.append(km)
            inDistanceRange.append((km < self.weatherSearchDistance).nonzero()[0])
        distances = np.asarray(distances)
        inDistanceRange = np.asarray(inDistanceRange)

        slider = self.weatherTimebar
        v = slider.valueSteps()
        sliderRange = v[1] - v[0]
        
        if self.weatherGenerateAll:
            # number of grids to generate based on timebar range
            nGrids = int(slider.steps() - sliderRange + 1)
            # show modal dialog
        else:
            nGrids = 1
        
        grids = []
        self.progressBarInit(None)
        for g in range(nGrids):
            if self.weatherGenerateAll:
                startTime = slider.stepsToValue(g)
                endTime = slider.stepsToValue(g + sliderRange)
            else:
                startTime, endTime = slider.value()
            inTimeRange = ((time >= startTime) & (time <= endTime)).nonzero()[0]
            grid = np.zeros(gridsize * gridsize)
            for i in range(gridsize * gridsize):
                inBoth = np.intersect1d(inDistanceRange[i], inTimeRange, assume_unique=True).astype('i8')
                if inBoth.size:
                    grid[i] = np.sum(distances[i][inBoth]**-self.weatherInversePower * param[inBoth], axis=0)/\
                            np.sum(distances[i][inBoth]**-self.weatherInversePower)
            grids.append(grid)
            self.progressBarAdvance(100 / nGrids, None)
        self.weatherGrids = np.asarray(grids)
        self.progressBarFinished(None)
        self._updateWeatherOverlay()


    def __del__(self):
        self.progressBarFinished(None)
        os.remove(self._weatherOverlayImagePath)
        self.map = None

    def commit(self):
        self.Outputs.selected_data.send(self.selection)
        self.Outputs.annotated_data.send(create_annotated_table(self.data, self._indices))

    @Inputs.data
    def set_data(self, data):
        self.data = data

        self.closeContext()

        if data is None or not len(data):
            return self.clear()

        domain = data is not None and data.domain
        for model in (self._latlon_model,
                      self._class_model,
                      self._color_model,
                      self._shape_model,
                      self._size_model,
                      self._label_model,
                      self._timeModel):
            model.set_domain(domain)

        lat, lon = find_lat_lon(data)
        if lat or lon:
            self._combo_lat.setCurrentIndex(-1 if lat is None else self._latlon_model.indexOf(lat))
            self._combo_lon.setCurrentIndex(-1 if lon is None else self._latlon_model.indexOf(lon))
            self.lat_attr = lat.name
            self.lon_attr = lon.name

        if data.domain.class_var:
            self.color_attr = data.domain.class_var.name
        elif len(self._color_model):
            self._combo_color.setCurrentIndex(0)
        if len(self._shape_model):
            self._combo_shape.setCurrentIndex(0)
        if len(self._size_model):
            self._combo_size.setCurrentIndex(0)
        if len(self._label_model):
            self._combo_label.setCurrentIndex(0)
        if len(self._class_model):
            self._combo_class.setCurrentIndex(0)
        if len(self._timeModel):
            self._combo_time.setCurrentIndex(0)

        self.openContext(data)

        self.map.setTimeData(None)
        self.map.setTimeBounds(None, None)

        self.map.set_data(self.data, self.lat_attr, self.lon_attr, update=False)
        # initialise time data bounds
        self._combo_time.activated.emit(self._combo_time.currentIndex())
        self.map.set_marker_color(self.color_attr, update=False)
        self.map.set_marker_label(self.label_attr, update=False)
        self.map.set_marker_shape(self.shape_attr, update=False)
        self.map.set_marker_size(self.size_attr, update=True)


    @Inputs.data_subset
    def set_subset(self, subset):
        self.map.set_subset_ids(subset.ids if subset is not None else np.array([]))

    def handleNewSignals(self):
        super().handleNewSignals()
        self.train_model()

    @Inputs.learner
    def set_learner(self, learner):
        self.learner = learner
        self.controls.class_attr.setEnabled(learner is not None)
        self.controls.class_attr.setToolTip(
            'Needs a Learner input for modelling.' if learner is None else '')

    @Inputs.weatherData
    def loadWeatherData(self, data):
        self.weatherData = data

        if data is None or not len(data):
            self.weatherData = None
            self.weatherLatAttr = None
            self.weatherLonAttr = None
            self.weatherTimeAttr = None
            self.weatherParamAttr = None
            self.weatherInterpType = 0
            for model in (self._weatherModel,
                          self._weatherTimeModel):
                model.set_domain(None)
            self.clearGrids
            self._comboWeatherTime.activated.emit(self._comboWeatherTime.currentIndex())
            return

        domain = data is not None and data.domain
        for model in (self._weatherModel,
                      self._weatherTimeModel):
            model.set_domain(domain)
            
        lat, lon = find_lat_lon(data)
        if lat or lon:
            self._comboWeatherLat.setCurrentIndex(-1 if lat is None else self._weatherModel.indexOf(lat))
            self._comboWeatherLon.setCurrentIndex(-1 if lon is None else self._weatherModel.indexOf(lon))
            self.weatherLatAttr = lat.name
            self.weatherLonAttr = lon.name
        else:
            self.weatherLatAttr = self.weatherLonAttr = self.weatherParamAttr = None

        if self.timeAttr is not None:
            self._comboWeatherTimestamp.setCurrentIndex(self._combo_timestamp.currentIndex())
        else:
            self._comboWeatherTimestamp.setCurrentIndex(0)
        if len(self._weatherTimeModel):
            self._comboWeatherTime.setCurrentIndex(0)
        else:
            self.weatherTimeAttr = None
        
        self.weatherParamAttr = None
        # initialise data
        self._comboWeatherTime.activated.emit(self._comboWeatherTime.currentIndex())

        self._dockWeather.show()

    def train_model(self):
        model = None
        self.Error.clear()
        if self.data and self.learner and self.class_attr != '(None)':
            domain = self.data.domain
            if self.lat_attr and self.lon_attr and self.class_attr in domain:
                domain = Domain([domain[self.lat_attr], domain[self.lon_attr]],
                                [domain[self.class_attr]])  # I am retarded
                train = Table.from_table(domain, self.data)
                try:
                    model = self.learner(train)
                except Exception as e:
                    self.Error.learner_error(e)
        self.map.set_model(model)

    def disable_some_controls(self, disabled):
        tooltip = (
            "Available when the zoom is close enough to have "
            "<{} points in the viewport.".format(self.map.N_POINTS_PER_ITER)
            if disabled else '')
        for widget in (self._combo_label,
                       self._combo_shape,
                       self._clustering_check):
            widget.setDisabled(disabled)
            widget.setToolTip(tooltip)

    def clear(self):
        self.map.set_data(None, '', '')
        for model in (self._latlon_model,
                      self._class_model,
                      self._color_model,
                      self._shape_model,
                      self._size_model,
                      self._label_model,
                      self._timeModel):
            model.set_domain(None)
        self._combo_time.activated.emit(self._combo_time.currentIndex())
        self.lat_attr = self.lon_attr = self.class_attr = self.color_attr = \
        self.label_attr = self.shape_attr = self.size_attr = None


def main():
    from AnyQt.QtWidgets import QApplication
    from Orange.modelling import KNNLearner as Learner
    a = QApplication([])

    ow = OWMap()
    ow.show()
    ow.raise_()
    data = Table("India_census_district_population")
    ow.set_data(data)

    QTimer.singleShot(10, lambda: ow.set_learner(Learner()))

    ow.handleNewSignals()
    a.exec()
    ow.saveSettings()

if __name__ == "__main__":
    main()
