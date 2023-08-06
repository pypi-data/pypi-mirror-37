from ..phone import phone_number


def BWCellNumber(value):
    regex = '^[7]{1}[12345678]{1}[0-9]{6}$'
    phone_number(value, regex, 'cell')


def BWTelephoneNumber(value):
    regex = '^[0-9+\(\)#\.\s\/ext-]+$'
    phone_number(value, regex, 'telephone')
