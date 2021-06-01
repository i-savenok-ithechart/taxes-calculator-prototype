from typing import Callable, Optional, Sequence, Union
from uuid import uuid4

from django.contrib.postgres import fields as postgres_fields
from django.db import models as _models
from django.db import transaction as _transaction


class Q(_models.Q):
    pass


class UUIDField(_models.UUIDField):
    pass


class EmailField(_models.EmailField):
    pass


class BooleanField(_models.BooleanField):
    pass


class CharField(_models.CharField):
    pass


class UrlField(_models.URLField):
    pass


class TextField(_models.TextField):
    pass


class ForeignKey(_models.ForeignKey):
    pass


class IntegerField(_models.IntegerField):
    pass


class StoryPointField(IntegerField):
    pass


class ManyToManyField(_models.ManyToManyField):
    pass


class OneToOneField(_models.OneToOneField):
    pass


class PositiveIntegerField(_models.PositiveIntegerField):
    pass


class DateField(_models.DateField):
    pass


class DateTimeField(_models.DateTimeField):
    pass


class SlugField(_models.SlugField):
    pass


class Max(_models.Max):
    pass


class JSONField(postgres_fields.JSONField):
    pass


class F(_models.F):
    pass


CASCADE: Callable = _models.CASCADE
SET_NULL: Callable = _models.SET_NULL
PROTECT: Callable = _models.PROTECT


class Model(_models.Model):
    id = UUIDField(primary_key=True, db_index=True, default=uuid4, editable=False)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    @property
    def short_id(self) -> str:
        return self.id.hex

    def after_each_save(self):
        pass

    def after_first_save(self):
        pass

    def save(  # type: ignore
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Union[Sequence[str], str]] = None
    ):
        self.clean()
        is_first_save = self.created_at is None

        super().save(force_insert, force_update, using, update_fields)

        if is_first_save:
            self.after_first_save()
        self.after_each_save()

    def before_delete(self):
        pass

    def delete(
        self,
        using: Optional[str] = None,
        keep_parents: bool = False
    ):
        self.before_delete()
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        abstract = True


atomic = _transaction.atomic


class Count(_models.Count):
    pass


class Prefetch(_models.Prefetch):
    pass


class Case(_models.Case):
    pass


class When(_models.When):
    pass


class DecimalField(_models.DecimalField):
    pass


class Manager(_models.Manager):
    pass


class QuerySet(_models.QuerySet):
    pass
