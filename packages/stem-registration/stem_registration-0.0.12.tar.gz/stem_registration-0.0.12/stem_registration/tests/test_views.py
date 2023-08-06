from cities_light.models import Country
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from stem_registration.models import RegistrationData


class TestRegistrationViewStem(TestCase):
    client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name='USA', continent='NA')
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")

    def test_get(self):
        try:
            # todo чтоб запускались тесы на установленном приложении и локально, разобраться как сделать универсально
            # response = self.client.get(reverse('stem:stem_register'))
            response = self.client.get(reverse('stem_register'))
        except:
            response = self.client.get(reverse('main:stem_register'))
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        data = {
            'username': 'test_user',
            'password1': 'dd@mailinator.com',
            'password2': 'dd@mailinator.com',
            'number': '+10955217581',
            'email': 'dd@mailinator.com',
            'first_name': 'Dmitriy',
            'last_name': 'Shevelev',
            'contractor_type': 'PP',
            'tax_number': '', 'file1': '', 'file2': '', 'file3': '', 'file4': '', 'file5': '', 
            'address': 'biblika 1g',
            'address_optional': '',
            'city': 'Kharkiv',
            'country': self.country.id,
            'zip': '5622',
            'same': 'on',
            'billing_address': 'biblika 1g',
            'bill_address_optional': 'biblika 1g',
            'bill_city': '', 'bill_zip': '', 'agree': 'on'
        }
        try:
            # todo чтоб запускались тесы на установленном приложении и локально, разобраться как сделать универсально
            # response = self.client.post(reverse('stem:stem_register'), data=data)
            response = self.client.post(reverse('stem_register'), data=data)
        except:
            response = self.client.post(reverse('main:stem_register'), data=data)
        self.assertEquals(response.status_code, 302)

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            self.fail('User is not created')

        try:
            data = RegistrationData.objects.get(user=user)
        except RegistrationData.DoesNotExist:
            self.fail('RegistrationData is not created')

        print(data)
