import logging

from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from libs.repos.utils import assign_code_reference
from signals.tags import set_tags
from schemas.build_backends import BuildBackend

_logger = logging.getLogger('polyaxon.signals.build_jobs')


def set_backend(instance):
    if not instance.backend and instance.specification:
        instance.backend = instance.specification.build.backend or BuildBackend.NATIVE


@receiver(pre_save, sender=BuildJob, dispatch_uid="build_job_pre_save")
@ignore_updates_pre
@ignore_raw
def build_job_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    set_tags(instance=instance)
    set_backend(instance=instance)
    assign_code_reference(instance)


@receiver(post_save, sender=BuildJob, dispatch_uid="build_job_post_save")
@ignore_updates
@ignore_raw
def build_job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)
