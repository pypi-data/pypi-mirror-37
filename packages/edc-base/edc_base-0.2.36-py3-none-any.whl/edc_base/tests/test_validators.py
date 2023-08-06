from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms
from django.test import TestCase
from django.core.exceptions import ValidationError, ImproperlyConfigured

from ..model_validators import (
    MaxConsentAgeValidator, CompareNumbersValidator, MinConsentAgeValidator)
from .models import TestValidatorModel


class TestValidationForm(forms.ModelForm):

    class Meta:
        model = TestValidatorModel
        fields = '__all__'


class TestValidators(TestCase):

    def test_min_age_validator(self):
        validator = MinConsentAgeValidator(18)
        self.assertRaises(
            ValidationError, validator, date.today() - relativedelta(years=17))
        self.assertIsNone(validator(date.today() - relativedelta(years=18)))
        self.assertIsNone(validator(date.today() - relativedelta(years=19)))

    def test_max_age_validator(self):
        validator = MaxConsentAgeValidator(64)
        self.assertRaises(
            ValidationError, validator, date.today() - relativedelta(years=65))
        self.assertIsNone(validator(date.today() - relativedelta(years=64)))
        self.assertIsNone(validator(date.today() - relativedelta(years=63)))

    def test_compare_numbers_gt(self):
        validator = CompareNumbersValidator(10, '>')
        self.assertRaises(ValidationError, validator, 9)
        self.assertRaises(ValidationError, validator, 10)
        self.assertIsNone(validator(11))

    def test_compare_numbers_gte(self):
        validator = CompareNumbersValidator(10, '>=')
        self.assertRaises(ValidationError, validator, 9)
        self.assertIsNone(validator(10))
        self.assertIsNone(validator(11))

    def test_compare_numbers_lt(self):
        validator = CompareNumbersValidator(10, '<')
        self.assertIsNone(validator(9))
        self.assertRaises(ValidationError, validator, 10)
        self.assertRaises(ValidationError, validator, 11)

    def test_compare_numbers_none2(self):
        self.assertRaises(TypeError, CompareNumbersValidator)

    def test_compare_numbers_no_value(self):
        self.assertRaises(
            ImproperlyConfigured, CompareNumbersValidator, None, '<')

    def test_compare_numbers_no_values(self):
        self.assertRaises(
            ImproperlyConfigured, CompareNumbersValidator, None, None)

    def test_compare_numbers_not_numbers(self):
        self.assertRaises(
            TypeError, CompareNumbersValidator, [1, 2], '<')  # nonsense
        self.assertRaises(
            TypeError, CompareNumbersValidator, 'ABC', '<')  # nonsense

    def test_age_of_consent(self):
        form = TestValidationForm(data={'consent_age': 17})
        self.assertFalse(form.is_valid())
        form = TestValidationForm(data={'consent_age': 18})
        self.assertTrue(form.is_valid())
        form = TestValidationForm(data={'consent_age': 64})
        self.assertTrue(form.is_valid())
        form = TestValidationForm(data={'consent_age': 65})
        self.assertFalse(form.is_valid())
