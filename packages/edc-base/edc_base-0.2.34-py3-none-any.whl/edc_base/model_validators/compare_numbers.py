from django.core.exceptions import ValidationError, ImproperlyConfigured


class CompareNumbersValidator():
    """Compares the given field value to a value/operator."""

    default_comparision_operator = None
    default_message = 'Expected value to be \'{}{}\'. Got {}.'

    def __init__(self, comparision_value, comparision_operator=None, message=None):
        self.comparision_operator = comparision_operator or self.default_comparision_operator
        if comparision_value:
            if not isinstance(comparision_value, (int, float)):
                raise TypeError('Expected to compare numbers. Got {}'.format(comparision_value))
        self.comparision_value = comparision_value
        self.message = message or self.default_message
        operators = ['<', '<=', '>', '>=', '!=']
        if self.comparision_value is None:
            raise ImproperlyConfigured(
                'Validator expected a comparison value. Got None.'.format(
                    ','.join(operators), self.comparision_operator))
        if self.comparision_operator not in operators:
            raise ImproperlyConfigured(
                'Validator expected operator to be one of {}. Got \'{}\'.'.format(
                    ','.join(operators), self.comparision_operator))

    def __call__(self, value):
        if self.comparision_value:
            try:
                if ((self.comparision_operator == '<' and value < self.comparision_value) or
                        (self.comparision_operator == '<=' and value <= self.comparision_value) or
                        (self.comparision_operator == '!=' and value != self.comparision_value) or
                        (self.comparision_operator == '>' and value > self.comparision_value) or
                        (self.comparision_operator == '>=' and value >= self.comparision_value)):
                    pass
                else:
                    message = self.message.format(
                        self.comparision_operator or 'None', self.comparision_value, value)
                    raise ValidationError(message)
            except TypeError as e:
                raise TypeError('Expected to compare numbers. {}'.format(e))
