#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2025  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cmk.graphing.v1 import (
    metrics,
    translations,
    graphs,
    perfometers,
)

translation_fsecure_status = translations.Translation(
    name="fsecure_status",
    check_commands=[translations.PassiveCheck("fsecure_status")],
    translations={
        "avdef_age": translations.RenameTo("fsecure_status_avdef_age"),
        "last_connection": translations.RenameTo("fsecure_status_last_connection"),
    },
)

metric_fsecure_status_avdef_age = metrics.Metric(
    name='fsecure_status_avdef_age',
    title=metrics.Title('AV Definition Age'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.LIGHT_GREEN,
)

metric_fsecure_status_last_connection = metrics.Metric(
    name='fsecure_status_last_connection',
    title=metrics.Title('Last Connection'),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.DARK_GREEN,
)

graph_fsecure_status_avdef_age = graphs.Graph(
    name="fsecure_status_avdef_age",
    title=graphs.Title("WithSecure Status - AV Definition Age"),
    minimal_range=graphs.MinimalRange(0, metrics.WarningOf(metric_name='fsecure_status_avdef_age')),
    compound_lines=['fsecure_status_avdef_age'],
    simple_lines=[
        metrics.WarningOf(metric_name='fsecure_status_avdef_age'),
        metrics.CriticalOf(metric_name='fsecure_status_avdef_age'),
    ],
)

graph_fsecure_status_last_connection = graphs.Graph(
    name="fsecure_status_last_connection",
    title=graphs.Title("WithSecure Status - Last Connection"),
    minimal_range=graphs.MinimalRange(0, metrics.WarningOf(metric_name='fsecure_status_last_connection')),
    compound_lines=['fsecure_status_last_connection'],
    simple_lines=[
        metrics.WarningOf(metric_name='fsecure_status_last_connection'),
        metrics.CriticalOf(metric_name='fsecure_status_last_connection'),
    ],
)

perfometer_name = perfometers.Perfometer(
    name="fsecure_status_avdef_age",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Closed(metrics.WarningOf(metric_name='fsecure_status_avdef_age'))),
    segments=["fsecure_status_avdef_age"],
)
