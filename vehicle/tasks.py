from celery import shared_task
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from vehicle.models import Car, Moto


@shared_task
def check_milage(pk, model):
    if model == 'Car':
        instance = Car.objects.first(pk=pk).first()
    else:
        instance = Moto.objects.first(pk=pk).first()

    if instance:
        prev_milage = -1
        for m in instance.milage.all():
            if prev_milage == -1:
                prev_milage = m.milage
            else:
                if prev_milage < m.milage:
                    raise ValidationError('Неверный пробег')


def check_filter():
    filter_amount = {'amount__lte': 500}

    if Car.objects.filter(**filter_amount).exists():
        print('отчет по фильтру')
