from django.db import models
from core.models import TimeStampedModel


class Contact(TimeStampedModel):
    first_name = models.CharField(max_length=128, )
    last_name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    email = models.EmailField()
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def export(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'city': self.city,
            'country': self.country,
            'phone_number': self.phone_number,
            'email': self.email,
            'date_of_birth': self.date_of_birth
        }
