# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import City, District, Ward
import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q


def address_format(address=''):
    try:
        address = json.loads(address)
    except (ValueError, SyntaxError):
        return False
    else:
        if len(address) == 5:
            if not (address.get('street_no', None) and address.get('street_name', None) and address.get('district_id', None) and address.get('city_id', None) and address.get('ward_id', None)):
                return False
            else:
                try:
                    street_no = address['street_no']
                    street_name = address['street_name']
                    ward_id = address['ward_id']
                    district_id = address['district_id']
                    city_id = address['city_id']

                    City.objects.get(pk=city_id)
                    District.objects.get(
                        Q(pk=district_id) & Q(city_id=city_id))
                    if ward_id:
                        Ward.objects.get(Q(pk=ward_id) & Q(
                            district_id=district_id))
                except (KeyError, ObjectDoesNotExist, ValidationError):
                    return False
                else:
                    if len(street_no) > 30 or len(street_name) > 150:
                        return False
                    return {
                        'street_no': street_no,
                        'street_name': street_name,
                        'ward_id': ward_id,
                        'district_id': district_id,
                        'city_id': city_id
                    }
        else:
            return False
