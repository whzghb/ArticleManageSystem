import django.dispatch
from utils.functions import model_to_zh
from common.models import Log

log = django.dispatch.Signal(providing_args=["admin", "model", "method"])


def callback(sender, **kwargs):
    kwargs.pop('signal')
    clean_model = kwargs['model'].split('.')[-1].split("'")[0]
    kwargs["model"] = model_to_zh(clean_model)
    Log.objects.create(**kwargs)


log.connect(callback)