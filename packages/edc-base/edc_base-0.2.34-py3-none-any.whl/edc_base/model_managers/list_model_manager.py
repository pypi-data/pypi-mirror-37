from django.db import models


class ListModelManager(models.Manager):

    def get_by_natural_key(self, short_name):
        return self.get(short_name=short_name)
