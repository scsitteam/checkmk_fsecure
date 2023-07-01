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

# <<<fsecure_status:sep(58)>>>
# RealTimeScanningEnabled: True
# DeepGuardEnabled: True
# BrowsingProtectionEnabled: True
# LastConnectionTimeInHoursAgo: 0
# AvDefinitionsAgeInHours: 44

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    check_levels,
    render,
)


def parse_fsecure_status(string_table):
    parsed = {}

    for key, val in string_table:
        val = val.lstrip()
        if val.isdigit():
            parsed[key] = int(val)
        elif val in ['Enabled', 'True']:
            parsed[key] = True
        elif val in ['Disabled', 'False']:
            parsed[key] = False
        else:
            parsed[key] = val
    return parsed


register.agent_section(
    name='fsecure_status',
    parse_function=parse_fsecure_status,
)


FSECURE_STATUS_CHECK_DEFAULT_PARAMETERS = {
    'last_connection': (12 * 60 * 60, 24 * 60 * 60),
    'avdef_age': (24 * 60 * 60, 48 * 60 * 60)
}


def discovery_fsecure_status(section):
    if section.get('RealTimeScanningEnabled', '') != '':
        yield Service()


def check_fsecure_status(params, section):
    if section['RealTimeScanningEnabled'] is True:
        yield Result(state=State.OK, summary='RealTimeScanning is enabled')
    else:
        yield Result(state=State.CRIT, summary='RealTimeScanning not enabled')

    if section['DeepGuardEnabled'] is True:
        yield Result(state=State.OK, summary='DeepGuard is enabled')
    else:
        yield Result(state=State.CRIT, summary='DeepGuard not enabled')

    if section['BrowsingProtectionEnabled'] is True:
        yield Result(state=State.OK, summary='BrowsingProtection is enabled')
    else:
        yield Result(state=State.CRIT, summary='BrowsingProtection not enabled')

    yield from check_levels(
        section['LastConnectionTimeInHoursAgo'] * 60 * 60,
        levels_upper=params['last_connection'],
        label='Last Connection Age',
        render_func=render.timespan,
        metric_name='last_connection',
    )

    yield from check_levels(
        section['AvDefinitionsAgeInHours'] * 60 * 60,
        levels_upper=params['avdef_age'],
        label='AV Definition Age',
        render_func=render.timespan,
        metric_name='avdef_age',
    )


register.check_plugin(
    name = 'fsecure_status',
    service_name = 'F-Secure Status',
    discovery_function = discovery_fsecure_status,
    check_function = check_fsecure_status,
    check_default_parameters = FSECURE_STATUS_CHECK_DEFAULT_PARAMETERS,
    check_ruleset_name = 'fsecure_status',
)
