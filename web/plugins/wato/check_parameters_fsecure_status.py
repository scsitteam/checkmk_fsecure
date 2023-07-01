#!/usr/bin/env python
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

from cmk.gui.exceptions import MKUserError
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    Tuple,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    RulespecGroupCheckParametersApplications,
    rulespec_registry,
)


def _validate_tuple_increase(value, varprefix):
    cur = value[0]
    for entry in value[1:]:
        if entry <= cur:
            raise MKUserError(varprefix,
                              _('Warning needs to be smaller then critical'))
        cur = entry


def _valuespec_spec_fsecure_status():
    return Dictionary(
        elements=[
            ('last_connection',
             Tuple(
                 title=_('Last Connection'),
                 help=_('Time since the last connection to the controller.'),
                 elements=[
                     Age(title=_('Warning at'),
                         display=['hours'],
                         default_value=12 * 60 * 60),
                     Age(title=_('Critical at'),
                         display=['hours'],
                         default_value=24 * 60 * 60),
                 ],
                 validate=_validate_tuple_increase,
             )),
            ('avdef_age',
             Tuple(
                 title=_('AV Definition Age'),
                 help=_('Age of the AV Definitions.'),
                 elements=[
                     Age(title=_('Warning at'),
                         display=['hours'],
                         default_value=24 * 60 * 60),
                     Age(title=_('Critical at'),
                         display=['hours'],
                         default_value=48 * 60 * 60),
                 ],
                 validate=_validate_tuple_increase,
             )),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name='fsecure_status',
        group=RulespecGroupCheckParametersApplications,
        parameter_valuespec=_valuespec_spec_fsecure_status,
        title=lambda: _('F-Secure Status'),
    ))
