import os
from django.test import TestCase
from quartet_templates import models
from quartet_capture.models import Rule, Step, Task, StepParameter
from quartet_capture.rules import Rule as CRule

class TemplateTest(TestCase):
    '''
    Tests the Template model.
    '''
    def create_template(self, name: str, content: str, description: str):
        return models.Template.objects.create(name=name, content=content, description=description)

    def test_template_creation(self):
        content = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:bla:bla">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:SpecialXML>
         <SomethingSpecial>{{ something_special }}</SomethingSpecial>
      </urn:SpecialXML>
   </soapenv:Body>
</soapenv:Envelope>
        '''
        template = self.create_template(name="Test Template", content=content, description="A Test Template")
        self.assertTrue(isinstance(template, models.Template))

    def test_template_rendering(self):
        content = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:bla:bla">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:SpecialXML>
         <SomethingSpecial>{{ something_special }}</SomethingSpecial>
      </urn:SpecialXML>
   </soapenv:Body>
</soapenv:Envelope>
        '''
        template = self.create_template(name="Test Template", content=content, description="A Test Template")
        rendered = template.render(context={"something_special": "Special Value"})
        expected = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:bla:bla">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:SpecialXML>
         <SomethingSpecial>Special Value</SomethingSpecial>
      </urn:SpecialXML>
   </soapenv:Body>
</soapenv:Envelope>
        '''
        self.assertEqual(expected, rendered)

    def test_steps(self):
        vals = range(1000000,1000100)
        self._create_test_template()
        db_rule, db_task, db_step = self._create_rule()
        c_rule = CRule(db_task.rule, db_task)
        c_rule.execute(vals)
        print(c_rule.data)
        
    def _create_rule(self):
        db_rule = Rule()
        db_rule.name = 'Test Rule'
        db_rule.description = 'Template test rule.'
        db_rule.save()

        # create a new step
        db_step = Step()
        db_step.name = 'handle template'
        db_step.description = 'Template test.'
        db_step.order = 1
        db_step.step_class = 'quartet_templates.steps.TemplateStep'
        db_step.rule = db_rule
        db_step.save()
        sp = StepParameter.objects.create(
            step=db_step,
            name="Template Name",
            value="Test Template"
        )
        db_task = Task(
            rule=db_rule,
            status='QUEUED',
        )
        return db_rule, db_task, db_step

    def _create_test_template(self):
        models.Template.objects.create(
            name="Test Template",
            description="A test template",
            content=self._get_file_data()
        )

    def _get_file_data(self):
        file_path = '../tests/data/test_template.xml'
        curpath = os.path.dirname(__file__)
        f = open(os.path.join(curpath, file_path))
        return f.read()