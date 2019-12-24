import base64
import six
import uuid
import imghdr
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Image field that enable image to be sent over REST API
    like text (Base64 string).
    """
    def to_internal_value(self, data: str) -> serializers.ImageField:
        """Decode string to internal value

        Parameters:
             data (str): String that need to be decoded.

        Returns:
            data (obj): Decoded string
        """
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = uuid.uuid4()
            file_extension = self.get_file_extension(str(file_name), decoded_file)
            complete_file_name = "{}.{}".format(file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    @staticmethod
    def get_file_extension(file_name: str, decoded_file: base64) -> str:
        """Determine file extension

        Parameters:
            file_name (str): Name of file
            decoded_file (obj): Decoded string

        Returns:
            extension (str): Name of extension
        """
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension
