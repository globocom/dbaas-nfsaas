# -*- coding: utf-8 -*-
from util.models import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from backup.models import Snapshot


class Group(BaseModel):
    infra = models.ForeignKey(
        'physical.DatabaseInfra', related_name="nfsaas_group", unique=True
    )
    resource_id = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return '{}: {}'.format(self.infra, self.resource_id)


class HostAttr(BaseModel):
    host = models.ForeignKey(
        'physical.Host', related_name="nfsaas_host_attributes"
    )
    nfsaas_export_id = models.CharField(
        verbose_name=_("Export ID"), max_length=10
    )
    nfsaas_path = models.CharField(verbose_name=_("Path"), max_length=100)
    nfsaas_path_host = models.CharField(
        verbose_name=_("Path Host"), max_length=100, default=''
    )
    is_active = models.BooleanField(
        verbose_name=_("Is instance active"), default=True
    )
    nfsaas_size_kb = models.IntegerField(
        verbose_name=_("Size KB"), null=True, blank=True
    )
    nfsaas_used_size_kb = models.IntegerField(
        verbose_name=_("Used size KB"), null=True, blank=True
    )
    group = models.ForeignKey(
        Group, related_name='hosts', null=True, blank=True
    )

    class Meta:
        verbose_name_plural = 'NFaaS Custom Host Attributes'

    def snapshots(self,):
        return Snapshot.objects.filter(
            export_path=self.nfsaas_path, purge_at=None
        )

    def __unicode__(self):
        return '{}'.format(self.nfsaas_path)
