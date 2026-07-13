import re
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:
        raise ValidationError('حداکثر حجم مجاز برای لوگو 2 مگابایت است.')

def validate_landline_phone(value):
    phone_regex = r'^0[1-9]\d{9}$'
    if not re.match(phone_regex, value):
        raise ValidationError('شماره تلفن ثابت وارد شده معتبر نیست. نمونه معتبر: 021XXXXXXXX')
