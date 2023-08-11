import re
from django.core.exceptions import ValidationError


def password_compair(password, confirm_password):
    if not password == confirm_password:
        raise ValidationError('رمز شما مطابقت ندارد')
    return password
