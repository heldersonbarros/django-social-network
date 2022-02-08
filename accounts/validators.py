from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image(image):
    width, height = get_image_dimensions(image)

    if width < 180 or width > 600:
        raise ValidationError("Width should be >= 180px and <= 600")
    if height < 180 or height > 600:
        raise ValidationError("Height should be >= 180px and <= 600")
                
    if image.size > 1024*1024:
        raise ValidationError("Image file too large ( > 1mb )")