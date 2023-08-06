from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models


class RegistrationData(models.Model):
    PRIVATE_PERSON = 'PP'
    COMPANY = 'CO'
    INDIVIDUAL_ENTREPRENEUR = 'IE'
    CONTRACTOR_TYPE = (
        (PRIVATE_PERSON, _('Частное лицо')),
        (COMPANY, _('Компания')),
        (INDIVIDUAL_ENTREPRENEUR, _('Частный предприниматель'))
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contractor_type = models.CharField(
        max_length=2, choices=CONTRACTOR_TYPE, default=PRIVATE_PERSON, null=False,
        verbose_name=_('Тип контрагента'),
        help_text=_(
            '<details>'
            '<ul>'
            '<li>Частное лицо: заполняем ФИО, ИНН - не обязательно. Наименование  = ФИО</li>'
            '<li>Частный предприниматель: заполняем ФИО, ИНН, полное наименование. Наименование  = ФИО (СПД-ФЛ)</li>'
            '<li>Компания: заполняем Наименование, Полное наименование, ИНН, ЕГРПОУ</li>'
            '</ul>'
            '</details>'
        ),
        blank=True,
    )
    # todo Перевести verbose_names
    address = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Адрес'))
    address_optional = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Адрес (доп.)'))
    country = models.ForeignKey(
        'cities_light.Country', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Страна'),
        help_text=_('Страна происхождения контрагента')
    )
    city = models.CharField(max_length=100, default='', blank=True, verbose_name=_('Город'))
    zip = models.CharField(max_length=50, default='', blank=True, verbose_name=_('Почтовый индекс'))
    # same = forms.BooleanField(widget=forms.CheckboxInput(), label=_("Same"),
    #                           required=False, initial=True)
    billing_address = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Адрес'))
    bill_address_optional = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Адрес'))
    bill_city = models.CharField(max_length=100, default='', blank=True, verbose_name=_('Город'))
    bill_zip = models.CharField(max_length=50, default='', blank=True, verbose_name=_('Почтовый индекс'))
    bill_country = models.ForeignKey(
        'cities_light.Country', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Страна'),
        help_text=_('Страна происхождения контрагента'),
        related_name='bill_countries',
    )
    # todo добавить PhoneField (надоли...)
    number = models.CharField(max_length=50, default='', blank=True, verbose_name=_('Номер телефона'))

    accounting_number = models.CharField(
        max_length=20, default='', blank=True, null=True,
        verbose_name=_('ЕГРПОУ'),
        help_text=_(
            '<details>для других страни или не используется или как-то иначе называется</details>')
    )

    name_legal = models.CharField(
        max_length=255, default='', blank=True,
        verbose_name=_('Полное наименование'),
        help_text=_('<details>Юридическое название компании, '
                    'частного или индивидуального предпринимателя.'
                    '<br>Для Частный лиц указывайте ФИО полностью'
                    '<br>Это поле используется при формировании печатных форм документов</details>')
    )
    tax_number = models.CharField(default='', max_length=12, blank=True, verbose_name=_('ИНН'))

    def clean(self):
        if (self.contractor_type == self.PRIVATE_PERSON or self.contractor_type == self.INDIVIDUAL_ENTREPRENEUR) \
                and len(self.tax_number) != 10:
            raise ValidationError(_("ИНН должен содержать 10 символов"))
        elif self.contractor_type == self.COMPANY and len(self.tax_number) != 12:
            raise ValidationError(_("ИНН должен содержать 12 символов"))

    def __str__(self):
        return '%s %s' % (self.user, self.contractor_type)
