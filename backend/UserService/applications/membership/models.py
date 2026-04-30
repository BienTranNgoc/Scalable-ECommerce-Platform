# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _

PRICE_UNIT = (
    ('VND/m', _('VND per month')), ('VND/y', _('VND per year')),
)

EXPIRED_TIME_UNIT = (
    ('d', _('day(s)')),
    ('m', _('month(s)')),
    ('y', _('year(s)')),
)

# Note: you have to add any services at the end
TYPE_OF_SERVICE = (
    ('cloud', 'Cloud Service'),
    ('maintenance', 'Maintenance/Warranty Service'),
)

TYPE_OF_PACKAGE = (
    (0, 'Basic'),
    (1, 'Premium'),
    (2, 'Basic for SME'),
    (3, 'Premium for SME'),
    (4, "Event snapshot"),
    (5, "Event snapshot for SME"),
    (6, "General for Family/SME"),
    (7, "Basic SE"),
    (8, "Basic SE for SME"),
    (9, "Free new camera with NVR"),
    (10, "Default")
)

MODEL_STATUS = (
    (True, 'active'),
    (False, 'deleted'),
)

BASIC = 0
PREMIUM = 1
SME_BASIC = 2
SME_PREMIUM = 3
EVENT_BASIC = 4
SME_EVENT_BASIC = 5
SE_BASIC = 7
SE_SME_BASIC = 8
FREE_PACKAGE = 9


FAMILY = 1
SME = 2
GENERAL = 6
BASIC_SE_CID = 999

LIST_NO_RENEW_TYPE_PACKAGE = [
    SE_BASIC, SE_SME_BASIC, FREE_PACKAGE, BASIC, SME_BASIC]
