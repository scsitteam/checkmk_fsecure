#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2025  Marius Rieder <marius.rieder@durchmesser.ch>
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

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    DefaultValue,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _parameter_form_fsecure_status_bakery():
    return Dictionary(
        elements={
            'agent': DictElement(
                parameter_form=SingleChoice(
                    title=Title('WithSecure Status Check'),
                    help_text=Help('This will deploy the agent plugin <tt>fsecure_status</tt> '
                                   'for checking WithSecure status on Windows.'),
                    elements=[
                        SingleChoiceElement(name='deploy', title=Title('Deploy WithSecure Status plugin')),
                        SingleChoiceElement(name='do_not_deploy', title=Title('Do not deploy WithSecure Status plugin')),
                    ],
                    prefill=DefaultValue('deploy'),
                ),
                required=True,
            )
        },
    )


rule_spec_fsecure_status_bakery = AgentConfig(
    title=Title('WithSecure Status Check'),
    name='fsecure_status',
    parameter_form=_parameter_form_fsecure_status_bakery,
    topic=Topic.APPLICATIONS,
    help_text=Help('This will deploy the agent plugin <tt>fsecure_status</tt> '
                   'for checking WithSecure status on Windows.'),
)
