#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# fsecure_status - F-Secure Status Check with WMI
#
# Copyright (C) 2023  Marius Rieder <marius.rieder@scs.ch>
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

import pytest
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import fsecure_status

EXAMPLE_STRING_TABLE = [
    ['RealTimeScanningEnabled', 'False'],
    ['DeepGuardEnabled', 'False'],
    ['BrowsingProtectionEnabled', 'False'],
    ['LastConnectionTimeInHoursAgo', '6'],
    ['AvDefinitionsAgeInHours', '12'],
]
EXAMPLE_SECTION = {
    'RealTimeScanningEnabled': False,
    'DeepGuardEnabled': False,
    'BrowsingProtectionEnabled': False,
    'LastConnectionTimeInHoursAgo': 6,
    'AvDefinitionsAgeInHours': 12,
}


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        EXAMPLE_STRING_TABLE,
        EXAMPLE_SECTION
    ),
])
def notest_parse_fsecure_status(string_table, result):
    assert fsecure_status.parse_fsecure_status(string_table) == result


@pytest.mark.parametrize('section, result', [
    ({}, []),
    (EXAMPLE_SECTION, [Service()]),
])
def notest_discovery_fsecure_status(section, result):
    assert list(fsecure_status.discovery_fsecure_status(section)) == result


@pytest.mark.parametrize('params, result', [
    (
        fsecure_status.FSECURE_STATUS_CHECK_DEFAULT_PARAMETERS,
        [
            Result(state=State.CRIT, summary='RealTimeScanning not enabled'),
            Result(state=State.CRIT, summary='DeepGuard not enabled'),
            Result(state=State.CRIT, summary='BrowsingProtection not enabled'),
            Result(state=State.OK, summary='Last Connection Age: 6 hours 0 minutes'),
            Metric('last_connection', 21600.0, levels=(43200.0, 86400.0)),
            Result(state=State.OK, summary='AV Definition Age: 12 hours 0 minutes'),
            Metric('avdef_age', 43200.0, levels=(86400.0, 172800.0)),
        ]
    ),
    (
        {'last_connection': ('fixed', (2 * 60 * 60, 24 * 60 * 60)), 'avdef_age': ('fixed', (5 * 60 * 60, 48 * 60 * 60))},
        [
            Result(state=State.CRIT, summary='RealTimeScanning not enabled'),
            Result(state=State.CRIT, summary='DeepGuard not enabled'),
            Result(state=State.CRIT, summary='BrowsingProtection not enabled'),
            Result(state=State.WARN, summary='Last Connection Age: 6 hours 0 minutes (warn/crit at 2 hours 0 minutes/1 day 0 hours)'),
            Metric('last_connection', 21600.0, levels=(7200.0, 86400.0)),
            Result(state=State.WARN, summary='AV Definition Age: 12 hours 0 minutes (warn/crit at 5 hours 0 minutes/2 days 0 hours)'),
            Metric('avdef_age', 43200.0, levels=(18000.0, 172800.0)),
        ]
    ),
    (
        {'last_connection': ('fixed', (2 * 60 * 60, 4 * 60 * 60)), 'avdef_age': ('fixed', (5 * 60 * 60, 10 * 60 * 60))},
        [
            Result(state=State.CRIT, summary='RealTimeScanning not enabled'),
            Result(state=State.CRIT, summary='DeepGuard not enabled'),
            Result(state=State.CRIT, summary='BrowsingProtection not enabled'),
            Result(state=State.CRIT, summary='Last Connection Age: 6 hours 0 minutes (warn/crit at 2 hours 0 minutes/4 hours 0 minutes)'),
            Metric('last_connection', 21600.0, levels=(7200.0, 14400.0)),
            Result(state=State.CRIT, summary='AV Definition Age: 12 hours 0 minutes (warn/crit at 5 hours 0 minutes/10 hours 0 minutes)'),
            Metric('avdef_age', 43200.0, levels=(18000.0, 36000.0)),
        ]
    ),
])
def notest_check_fsecure_status(params, result):
    assert list(fsecure_status.check_fsecure_status(params, EXAMPLE_SECTION)) == result
