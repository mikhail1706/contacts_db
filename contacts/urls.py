from django.urls import path
from . import views

urlpatterns = [
    path('', views.Contacts.as_view(), name='contacts'),
    path('all/', views.GetContact.as_view(), name='contacts_json'),
    path('create/', views.ContactCreate.as_view(), name='contact_create')
]