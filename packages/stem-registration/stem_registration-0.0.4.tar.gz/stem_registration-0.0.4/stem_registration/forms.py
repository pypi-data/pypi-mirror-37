from django.contrib.auth.models import User
from registration.forms import RegistrationFormUniqueEmail
from django.forms.fields import CharField, ImageField

from django import forms
from django.utils.translation import ugettext as _

from stem_registration.models import RegistrationData


class RegistrationForm(RegistrationFormUniqueEmail):
    contractor_type = forms.ChoiceField(
        choices=RegistrationData.CONTRACTOR_TYPE,
        widget=forms.RadioSelect(),
        label=_("Компания"), initial=RegistrationData.PRIVATE_PERSON
    )
    address = CharField(max_length=30, label=_("Адрес"))
    address_optional = CharField(max_length=30, required=False, label=_("Адрес дополнительно"))
    city = CharField(max_length=30, label=_("Город"))
    zip = CharField(max_length=30, label=_("Индекс"))
    same = forms.BooleanField(widget=forms.CheckboxInput(), label=_("Same"),
                              required=False, initial=True)
    billing_address = CharField(max_length=30, required=False, label=_("Адрес"))
    bill_address_optional = CharField(max_length=30, required=False, label=_("Адрес дополнительно"))
    bill_city = CharField(max_length=30, required=False, label=_("Город"))
    bill_zip = CharField(max_length=30, required=False, label=_("Индекс"))
    number = CharField(max_length=30, label=_("Номер телефона"), required=True)
    tax_number = CharField(max_length=12, required=False, label=_('ИНН'))
    file1 = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
    file2 = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
    file3 = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
    file4 = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))
    file5 = ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none file'}))

    # def clean_tax_number(self):
    #     tax_number = self.data['tax_number']
    #     if (self.data['contractor_type'] == 'PP' or self.data['contractor_type'] == 'IE') and len(tax_number) != 10:
    #         raise forms.ValidationError("ИНН должен содержать 10 символов")
    #     elif self.data['contractor_type'] == 'CO' and len(tax_number) != 12:
    #         raise forms.ValidationError("ИНН должен содержать 12 символов")
    #     return tax_number

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'billing_address',
            'number',
            'tax_number',
            # 'accounting_number', 'name_legal',  # ????
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save()

        fields = (
            'contractor_type',
            'address',
            'address_optional',
            'country',
            'city',
            'zip',
            'billing_address',
            'bill_address_optional',
            'bill_city',
            'bill_zip',
            'number',
            'tax_number',
        )

        registration_data = {}
        for item in self.cleaned_data:
            if item in fields:
                registration_data[item] = self.cleaned_data[item]

        RegistrationData.objects.create(user=user, **registration_data)

        if commit:
            user.save()
            return user
