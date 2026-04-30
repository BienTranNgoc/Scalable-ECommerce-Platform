# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..users.models import Customer


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    order = models.PositiveIntegerField(
        default=1, verbose_name=_('Order number'))
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    city = models.ForeignKey(
        City, related_name='district_city', on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    order = models.PositiveIntegerField(
        default=1, verbose_name=_('Order number'))
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.city, self.name)

    def __str__(self):
        return u"{}-{}".format(self.city, self.name)


class Ward(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    district = models.ForeignKey(
        District, related_name='ward_district', on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    order = models.PositiveIntegerField(
        default=1, verbose_name=_('Order number'))
    status = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.district, self.name)

    def __str__(self):
        return u"{}-{}".format(self.district, self.name)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, related_name='address_customer', on_delete=models.CASCADE)
    street_no = models.TextField(max_length=30)
    street_name = models.TextField(max_length=150)
    city = models.ForeignKey(
        City, related_name='address_city', on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, related_name='address_district', on_delete=models.CASCADE)
    ward = models.ForeignKey(
        Ward, related_name='address_ward', on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return '{}, {}, {}'.format(self.city, self.district.name, self.ward.name)

    def __str__(self):
        return u'{}, {}, {}'.format(self.city, self.district.name, self.ward.name)
