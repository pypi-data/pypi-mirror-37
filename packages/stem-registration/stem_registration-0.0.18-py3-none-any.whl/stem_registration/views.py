from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from registration.backends.default.views import RegistrationView

from stem_registration.forms import RegistrationForm


class RegistrationViewStem(RegistrationView):
    form_class = RegistrationForm

    # country = Country.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class,
            # 'country': self.country
        })

    def post(self, request, *args, **kwargs):

        form_class = self.form_class(request.POST, request.FILES)

        client_presave = super(RegistrationViewStem, self)
        if form_class.is_valid():
            client = client_presave.register(form_class)

            # if request.POST.get('contractor_type') == 'PP':
            #     DocumentImages.objects.create(documents_files=form_class.cleaned_data['file1'],
            #                                   user_profile=client)
            #     DocumentImages.objects.create(documents_files=form_class.cleaned_data['file2'],
            #                                   user_profile=client)
            #     DocumentImages.objects.create(documents_files=form_class.cleaned_data['file3'],
            #                                   user_profile=client)
            #     DocumentImages.objects.create(documents_files=form_class.cleaned_data['file4'],
            #                                   user_profile=client)
            #
            # elif request.POST.get('contractor_type') == 'IE':
            #     DocumentImages.objects.create(documents_files=request.FILES.get('file1'), user_profile_id=client.id)
            #
            # phone = Phone.objects.create(content_object=client, source=client.username,
            #                              number=form_class.cleaned_data['number'],
            #                              created_by=client.username)
            # address = Address.objects.create(content_object=client, source=client.username,
            #                                  address=form_class.cleaned_data['address'],
            #                                  address_optional=form_class.cleaned_data['address_optional'],
            #                                  country_id=request.POST.get('country'),
            #                                  city=form_class.cleaned_data['city'],
            #                                  zip=form_class.cleaned_data['zip'],
            #                                  created_by=client.username)
            # email = Email.objects.create(content_object=client, source=client.username, created_by=client.username,
            #                              email=form_class.cleaned_data['email'])
            #
            # if not request.POST.get('same'):
            #     billing_address = Address.objects.create(content_object=client, source=client.username,
            #                                              address=form_class.cleaned_data['billing_address'],
            #                                              address_optional=form_class.cleaned_data[
            #                                                  'bill_address_optional'],
            #                                              country_id=request.POST.get('country'),
            #                                              city=form_class.cleaned_data['bill_city'],
            #                                              zip=form_class.cleaned_data['bill_zip'],
            #                                              created_by=client.username)
            # else:
            #     billing_address = address
            #
            # customer = Customer.objects.create(contractor_type=form_class.cleaned_data['contractor_type'],
            #                                    name=form_class.cleaned_data['name_legal'],
            #                                    name_legal=form_class.cleaned_data['name_legal'],
            #                                    tax_number=form_class.cleaned_data['tax_number'],
            #                                    accounting_number=form_class.cleaned_data['accounting_number'],
            #                                    prefix_code='',
            #                                    country_id=request.POST.get('country'),
            #                                    main_email_id=email.id,
            #                                    bill_address_id=billing_address.id,
            #                                    ship_address_id=address.id,
            #                                    created_by=client.username,
            #                                    source=client.username, )
            #
            # country = Country.objects.get(id=request.POST.get('country'))
            #
            # phone_customer = Phone.objects.create(content_object=customer, source=client.username,
            #                                       number=form_class.cleaned_data['number'],
            #                                       created_by=client.username)
            #
            # address_customer = Address.objects.create(content_object=customer, source=client.username,
            #                                           address=form_class.cleaned_data['address'],
            #                                           address_optional=form_class.cleaned_data['address_optional'],
            #                                           country_id=request.POST.get('country'),
            #                                           city=form_class.cleaned_data['city'],
            #                                           zip=form_class.cleaned_data['zip'],
            #                                           created_by=client.username)
            #
            # email_customer = Email.objects.create(content_object=customer, source=client.username,
            #                                       created_by=client.username,
            #                                       email=form_class.cleaned_data['email'])
            #
            # if not request.POST.get('same'):
            #     billing_address_customer = Address.objects.create(content_object=customer, source=client.username,
            #                                                       address=form_class.cleaned_data['billing_address'],
            #                                                       address_optional=form_class.cleaned_data[
            #                                                           'bill_address_optional'],
            #                                                       country_id=request.POST.get('country'),
            #                                                       city=form_class.cleaned_data['bill_city'],
            #                                                       zip=form_class.cleaned_data['bill_zip'],
            #                                                       created_by=client.username)
            # else:
            #     billing_address_customer = address_customer
            #
            # notification = Notification.objects.create(send_to_browser=True, send_to_telegram=phone_customer,
            #                                            send_to_viber=phone_customer,
            #                                            send_to_email=email, send_to_sms=phone_customer)

            # customer.main_phone = phone_customer
            # customer.main_customer = customer
            # customer.ship_address = address_customer
            # customer.bill_address = billing_address_customer
            # customer.main_email = email_customer
            # customer.save()
            #
            # client.ship_address = address
            # client.notification = notification
            # client.bill_address = billing_address
            # client.main_phone = phone
            # client.main_email = email
            # client.country = country
            # client.main_customer = customer
            client.save()
            return HttpResponseRedirect(reverse('registration_complete'))

        return render(request, self.template_name, {
            'form': form_class,
            # 'country': self.country
        })
