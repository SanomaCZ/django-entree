from django.db.models.base import Model
from django.db.models.signals import pre_delete, pre_save


def _flush_cached(sender, **kwargs):
    sender.objects.flush_cached(key=kwargs['instance'].cache_key)


class CachedModel(Model):
    class Meta:
        abstract = True

    @property
    def cache_key(self):
        return self.pk

    def __init__(self, *args, **kwargs):
        pre_delete.connect(_flush_cached, sender=self.__class__)
        pre_save.connect(_flush_cached, sender=self.__class__)
        super(CachedModel, self).__init__(*args, **kwargs)
