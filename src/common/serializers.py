from rest_framework import serializers as _serializers


class Serializer(_serializers.Serializer):  # noqa
    pass


class DecimalField(_serializers.DecimalField):
    pass
