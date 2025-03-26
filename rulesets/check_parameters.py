#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# fsecure_status - F-Secure Status Check with WMI
#
# Copyright (C) 2023-2025  Marius Rieder <marius.rieder@scs.ch>
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


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    LevelDirection,
    migrate_to_float_simple_levels,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostCondition


def _parameter_form_fsecure_status():
    return Dictionary(
        elements={
            'last_connection': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Last Connection'),
                    help_text=Help('Time since the last connection to the controller.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE]
                    ),
                    migrate=migrate_to_float_simple_levels,
                    prefill_fixed_levels=InputHint(value=(12 * 60 * 60, 24 * 60 * 60)),
                ),
                required=False,
            ),
            'avdef_age': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('AV Definition Age'),
                    help_text=Help('Age of the AV Definitions.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE]
                    ),
                    migrate=migrate_to_float_simple_levels,
                    prefill_fixed_levels=InputHint(value=(24 * 60 * 60, 48 * 60 * 60)),
                ),
                required=False,
            ),
        },
    )


rule_spec_fsecure_status = CheckParameters(
    name='fsecure_status',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_fsecure_status,
    title=Title('WithSecure Status Levels'),
    help_text=Help('This rule configures thresholds for the WithSecure Status check.'),
    condition=HostCondition(),
)
