from django.core.exceptions import ValidationError

from edc_constants.constants import YES, NO, POS, NEG, DECLINED, MALE, FEMALE, UNKNOWN


def eligible_if_yes(value):
    if value != YES:
        raise ValidationError('Participant is NOT ELIGIBLE. Registration cannot continue.')


def eligible_if_yes_or_declined(value):
    if value not in [YES, DECLINED]:
        raise ValidationError('Please provide the subject with a copy of the consent.')


def eligible_if_no(value):
    if value != NO:
        raise ValidationError('Participant is NOT ELIGIBLE. Registration cannot continue.')


def eligible_if_unknown(value):
    if value != UNKNOWN:
        raise ValidationError('Participant is NOT ELIGIBLE. Registration cannot continue.')


def eligible_if_female(value):
    if value != FEMALE:
        raise ValidationError(
            'If gender not Female, Participant is NOT ELIGIBLE and registration cannot continue.')


def eligible_if_male(value):
    if value != MALE:
        raise ValidationError(
            'If gender not Male, Participant is NOT ELIGIBLE and registration cannot continue.')


def eligible_if_negative(value):
    if value != NEG:
        raise ValidationError(
            'Participant must be HIV Negative. Participant is NOT ELIGIBLE and registration cannot continue.')


def eligible_if_positive(value):
    if value != POS:
        raise ValidationError(
            'Participant must be HIV Positive. Participant is NOT ELIGIBLE and registration cannot continue.')


def eligible_not_positive(value):
    if value == POS:
        raise ValidationError(
            'Participant must be HIV Negative / Unknown. Participant is '
            'NOT ELIGIBLE and registration cannot continue.')
