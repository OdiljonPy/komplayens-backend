import os
from django.core.exceptions import ValidationError


def validate_file_type_and_size(value):
    """
    Validates the file type and size of uploaded files.

    Allowed types: PDF, Word, Excel
    Maximum size: 5MB
    """
    allowed_extensions = ['.pdf', '.mp4', '.mov', '.avi', '.mkv', '.flv', '.ppt', '.pptx']
    max_file_size = 50 * 1024 * 1024  # 50 MB

    # Get file extension
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed types are: {', '.join(allowed_extensions)}")

    # Check file size
    if value.size > max_file_size:
        raise ValidationError(f"The file size exceeds the 5MB limit.")
