import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DeleteView

from core.views import BaseView
from .models import Contact

error_logger = logging.getLogger('error_logger')


class Contacts(TemplateView):
    template_name = 'contacts/contacts.html'


class GetContact(BaseView):
    def get(self, request):
        result = {'data': {
            'headers': [],
            'contacts': [],
            'cities': [],
            'countries': [],
        }, 'msg': 'Success!', 'success': True}

        contacts = Contact.objects.all()
        result['data']['cities'] = list(contacts.distinct().values_list('city', flat=True))
        result['data']['countries'] = list(contacts.distinct().values_list('country', flat=True))

        result['data']['headers'] = [
            {'text': 'First Name', 'align': 'start', 'sortable': False, 'value': 'first_name'},
            {'text': 'Last Name', 'value': 'last_name'},
            {'text': 'City', 'value': 'city'},
            {'text': 'Country', 'value': 'country'},
            {'text': 'Phone number', 'value': 'phone_number'},
            {'text': 'Email', 'value': 'email'},
            {'text': 'Date of birth', 'value': 'date_of_birth'},
            {'text': 'Actions', 'value': 'actions', 'sortable': False},
        ]

        for contact in contacts:
            result['data']['contacts'].append(contact.export())

        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class ContactCreate(BaseView):
    def post(self, request):
        result = {'data': {}, 'msg': 'The contact has been created!', 'success': True}
        data = json.loads(request.body.decode('utf-8'))

        try:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            phone_number = data['phone_number']
            city = data.get('city')
            country = data.get('country')
            date_of_birth = data.get('date_of_birth')
        except KeyError as error:
            result['success'] = False
            result['msg'] = f'This information was not found {str(error)}'
            error_logger.error(f'Key error: {str(error)}')
            return JsonResponse(result)

        result['data']['new_contact'] = Contact.objects.create(first_name=first_name, last_name=last_name,
                                                               city=city, country=country,
                                                               phone_number=phone_number, email=email,
                                                               date_of_birth=date_of_birth).export()

        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class ContactUpdate(BaseView):
    def post(self, request, contact_id):
        result = {'data': '', 'msg': 'The contact has been updated', 'success': True}
        data = json.loads(request.body.decode('utf-8'))

        try:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            phone_number = data['phone_number']
            city = data.get('city')
            country = data.get('country')
            data_of_birth = data.get('data_of_birth')
        except KeyError as error:
            result['success'] = False
            result['msg'] = f'This information was not found {str(error)}'
            error_logger.error(f'Key error: {str(error)}')
            return JsonResponse(result)

        try:
            contact = Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            result['success'] = False
            result['msg'] = f'This contact was not found.'
            error_logger.error(f'Contact does not exist. Id: {contact_id}')
            return JsonResponse(result)

        contact.first_name = first_name
        contact.last_name = last_name
        contact.email = email
        contact.phone_number = phone_number
        contact.city = city
        contact.country = country
        contact.date_of_birth = data_of_birth
        contact.save()

        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class ContactDelete(DeleteView, BaseView):
    def delete(self, request, *args, **kwargs):
        result = {'data': '', 'msg': 'The contact has been deleted ', 'success': True}
        super(ContactDelete, self).delete(request, *args, **kwargs)
        return JsonResponse(result)
