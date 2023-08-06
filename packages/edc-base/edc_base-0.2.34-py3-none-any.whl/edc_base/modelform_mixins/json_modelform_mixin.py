import json


class JSONModelFormMixin:

    def as_json(self):
        """Dumps the form fields and labels to JSON.

        Call in modeladmin.save_model to capture form presented to user.
        """
        as_json = {}
        for field in self.base_fields.items():
            as_json[field[0]] = field[1].label
        return json.dumps([self._meta.model._meta.label_lower, as_json])
