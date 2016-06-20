from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.dispatch import receiver
from reversion.models import Version
from reversion.revisions import default_revision_manager

global_save_signal_receiver = []


class PreSaveHandler(object):
    def __init__(self, model_inst):
        super(PreSaveHandler, self).__init__()
        self.model_inst = model_inst

    def object_save_handler(self, sender, instance, **kwargs):
        # logging.error("======================================")
        if not (instance.pk is None):
            content_type = ContentType.objects.get_for_model(self.model_inst)
            versioned_pk_queryset = Version.objects.filter(content_type=content_type).filter(object_id_int=instance.pk)
            if not versioned_pk_queryset.exists():
                item = self.model_inst.objects.get(pk=instance.pk)
                try:
                    default_revision_manager.save_revision((item,))
                except:
                    pass


def add_reversion_before_save(model_inst):
    s = PreSaveHandler(model_inst)
    global_save_signal_receiver.append(s)
    receiver(pre_save, sender=model_inst)(s.object_save_handler)
