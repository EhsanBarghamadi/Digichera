from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:
        raise ValidationError('حداکثر حجم مجاز برای تصویر محصول 2 مگابایت است.')
