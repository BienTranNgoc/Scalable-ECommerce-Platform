# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models import JSONField


SEX_CHOICE = (
    ('male', _('Male')),
    ('female', _('Female'))
)

LANGUAGE_CHOICE = (
    ('vi', _('Vietnamese')),
    ('en', _('English'))
)


class PhoneNumberAbstactUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    sex = models.CharField(
        choices=SEX_CHOICE, max_length=6, blank=True, null=True)
    native_language = models.CharField(
        choices=LANGUAGE_CHOICE, max_length=2, default=LANGUAGE_CHOICE[0][0])
    status = models.BooleanField(default=True)
    max_place = models.SmallIntegerField(default=settings.MAX_PLACES_IN_USER)
    avatar = ThumbnailerImageField(
        upload_to=settings.UPLOAD_AVATAR_FOLDER,
        blank=True,
        null=True,
        default="")

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class Customer(PhoneNumberAbstactUser):
    REQUIRED_FIELDS = ['email']
    sso_status = models.BooleanField(default=False)
    verify_KYC = models.BooleanField(default=False)
    KYC_pending = models.BooleanField(default=False)
    KYC_by = models.CharField(max_length=100, blank=True, null=True)
    rogo_id = models.CharField(
        max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Customer account')
        verbose_name_plural = _('Customer accounts')

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)

    def update_customer(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        self.save()

    @classmethod
    def create_customer(cls, **kwargs):
        cls(**kwargs).save()

    @classmethod
    def find_customer(cls, **kwargs):
        return cls.objects.filter(**kwargs, is_active=True).first()


TYPE_PROFILE_CHOICE = (
    ('passport', _('Passport')),
    ('new', _('ID-Card 12 digits')),
    ('old', _('ID-Card 9 digits')),
)


class ProfileKYC(models.Model):
    # Required for each record
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.OneToOneField(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name=_('Birthday'))
    sex = models.CharField(
        choices=SEX_CHOICE, max_length=6, blank=True, null=True)
    id_card = models.CharField(max_length=12, verbose_name=_('Identification'))
    issue_date = models.DateField(verbose_name=_('Issued Date'))
    issue_loc = models.CharField(
        max_length=100, verbose_name=_('Issued location'))

    # Field for passport
    passport_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('Passport Number'))
    issue_expired = models.DateField(
        blank=True, null=True, verbose_name=_('Date of expiry'))
    pob = models.CharField(blank=True, null=True,
                           max_length=100, verbose_name=_("Place of birth"))
    nationality = models.CharField(blank=True, null=True, max_length=100)
    # Field for ID card
    home = models.CharField(blank=True, null=True,
                            max_length=100, verbose_name=_('Domicile'))
    address = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_('Place of residence'))

    # Type profile
    type_profile = models.CharField(
        max_length=50, choices=TYPE_PROFILE_CHOICE, blank=True, null=True)

    # Image information
    id_image = models.CharField(max_length=350, blank=True, null=True)
    back_id_image = models.CharField(max_length=350, blank=True, null=True)
    passport_image = models.CharField(max_length=350, blank=True, null=True)
    portrait_image = models.CharField(max_length=350, blank=True, null=True)

    # support information
    reason = models.CharField(max_length=1000, blank=True, null=True)
    supporter_email = models.CharField(max_length=100, blank=True, null=True)

    # Time
    create_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name=_('Create at'))
    verify_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Verify at'))
    last_modify = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Last edit'))
    matching_predicted = JSONField(blank=True, null=True)
