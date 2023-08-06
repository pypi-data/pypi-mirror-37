from django.db import models
from django.db.models.fields import AutoField
from simple_history.models import HistoricalRecords as SimpleHistoricalRecords
from django.utils.timezone import now


class SerializableModelManager(models.Manager):

    def get_by_natural_key(self, history_id):
        return self.get(history_id=history_id)


class SerializableModel(models.Model):

    objects = SerializableModelManager()

    def natural_key(self):
        return (self.history_id, )

    class Meta:
        abstract = True


class HistoricalRecords(SimpleHistoricalRecords):

    """HistoricalRecords that uses a UUID primary key
    and has a natural key method.
    """

    model_cls = SerializableModel

    def __init__(self, **kwargs):
        kwargs.update(bases=(self.model_cls, ))
        super().__init__(**kwargs)

    def get_history_id_field(self, model):
        """Return a field instance without initially assuming
        it should be AutoField.

        For example, primary key is UUIDField(
            primary_key=True, default=uuid.uuid4).
        """
        try:
            field = [
                field for field in model._meta.fields if field.primary_key][0]
            field = field.__class__(primary_key=True, default=field.default)
        except (IndexError, TypeError):
            field = AutoField(primary_key=True)
        return field

    def get_extra_fields(self, model, fields):
        """Overridden to set history_id (to UUIDField).
        """
        extra_fields = super().get_extra_fields(model, fields)
        extra_fields.update({'history_id': self.get_history_id_field(model)})
        extra_fields.update({'natural_key': lambda x: (x.history_id, )})
        return extra_fields
