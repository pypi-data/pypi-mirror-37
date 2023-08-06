from django.db import models

from .historical_records import HistoricalRecords


class HistoryManagerMixin(models.Model):

    history = HistoricalRecords()

    class Meta:
        abstract = True
