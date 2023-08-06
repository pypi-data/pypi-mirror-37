
class ReadonlyFieldsFormMixin:

    """Changes form fields to readonly/not required regardless
    of model attrs.

    By default sets all fields.

    User must ensure fields that cannot be null at DB level have value.
    """

    def get_readonly_fields(self):
        """Returns a tuple of field names.
        """
        return (key for key in self.fields)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.get_readonly_fields():
            self.fields[key].widget.attrs['readonly'] = True
            self.fields[key].required = False
