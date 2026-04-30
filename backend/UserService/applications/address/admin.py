# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from ..address.models import City, District, Ward, Address


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('customer', 'city', 'district', 'ward', 'street_name', 'street_no', 'is_default')

	def __init__(self, *args, **kwargs):
		super(AddressForm, self).__init__(*args, **kwargs)
		self.fields['city'].queryset = City.objects.all().order_by('name')
		self.fields['district'].queryset = District.objects.all().order_by('city__name')
		self.fields['ward'].queryset = Ward.objects.all().order_by('district__city__name', 'district__name')

	def clean_district(self):
		city = self.cleaned_data.get('city', None)
		district = self.cleaned_data.get('district', None)
		if city:
			if district.city != city:
				raise forms.ValidationError('District is not in "{}" city'.format(city.name))
		return district

	def clean_ward(self):
		district = self.cleaned_data.get('district', None)
		ward = self.cleaned_data.get('ward', None)
		if district and ward:
			if ward.district != district:
				raise forms.ValidationError('Ward is not in "{}" city'.format(district.name))
		return ward


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	form = AddressForm
	list_display = ('customer', 'city_name', 'district_name', 'ward_name', 'street_name', 'street_no', 'is_default')
	search_fields = ('customer__username',)

	def has_add_permission(self, request, *args, **kwargs):
		return True

	def city_name(self, obj):
		return obj.city.name

	def district_name(self, obj):
		return obj.district.name

	def ward_name(self, obj):
		return obj.ward.name


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	fields = ('name', 'order', 'status')
	list_display = ('name', 'lat', 'lon', 'order', 'status')
	search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
	fields = ('name', 'order', 'status')
	list_display = ('name', 'lat', 'lon', 'order', 'status')
	search_fields = ('name',)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
	fields = ('name', 'order', 'status')
	list_display = ('name', 'lat', 'lon', 'order', 'status')
	search_fields = ('name',)
