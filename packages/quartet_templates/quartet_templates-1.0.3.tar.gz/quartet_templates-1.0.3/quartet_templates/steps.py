# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.

from quartet_templates.models import Template
from quartet_capture.rules import Step, RuleContext


class TemplateStep(Step):
    """
    Will load a template based on the step parameter "Template Name" and
    render it using a combination of rule data, context variables and
    the template variables.
    """

    def execute(self, data, rule_context: RuleContext):
        self.info('Looking for Step Parameter with name "Template Name"...')
        template_name = self.get_parameter(
            'Template Name',
            raise_exception=True
        )
        self.info("Template Name parameter value found: %s.  "
                  "Looking up Template...", template_name)
        template = Template.objects.get(name=template_name)
        self.info("Found template...rendering...")
        data = template.render({'data':data, 'rule_context': rule_context,
                                'step_parameters':self.parameters,
                                'task_parameters':self.get_task_parameters(
                                    rule_context
                                )})
        self.info("Template response summary %s:", data[:10000])
        return data

    @property
    def declared_parameters(self):
        return {
            "Template Name": "The name of the template to load and render."
        }

    def on_failure(self):
        pass

