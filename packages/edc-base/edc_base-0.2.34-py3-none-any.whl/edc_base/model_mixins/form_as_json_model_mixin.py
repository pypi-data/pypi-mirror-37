import json

from django.db import models


class FormAsJSONModelMixin(models.Model):

    form_as_json = models.TextField(
        null=True,
        editable=False,
        help_text=(
            'System field to save form.as_json. form.as_json '
            'should be called in modeladmin.save_model'))

    def load_form(self):
        """Returns a JSON object."""
        if self.form_as_json:
            return json.loads(self.form_as_json)
        return None

    class Meta:
        abstract = True
