from datetime import date
from dateutil.relativedelta import relativedelta

from .compare_numbers import CompareNumbersValidator


class MinConsentAgeValidator(CompareNumbersValidator):

    default_comparision_operator = '>='
    default_message = 'The minimum age of consent is {}{} years. Got {}'

    def __call__(self, dob):
        rdelta = relativedelta(date.today(), dob)
        return CompareNumbersValidator(
            self.comparision_value, self.comparision_operator).__call__(rdelta.years)


class MaxConsentAgeValidator(CompareNumbersValidator):

    default_comparision_operator = '<='
    default_message = 'The maximum age of consent is {}{} years. Got {}'

    def __call__(self, dob):
        rdelta = relativedelta(date.today(), dob)
        return CompareNumbersValidator(
            self.comparision_value, self.comparision_operator).__call__(rdelta.years)
