from django.core import validators as django_validators


class MaxValueValidator(django_validators.MaxValueValidator):
    pass


class MinValueValidator(django_validators.MinValueValidator):
    pass
