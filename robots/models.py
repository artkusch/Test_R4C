from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order

class Robot(models.Model):
    count_week = models.IntegerField(blank=False, null=False)
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)



@receiver(post_save, sender=Robot)
def robot_created(sender, instance, **kwargs):
    print('new robot')

    robot_model = instance.model
    robot_version = instance.version
    robot_serial = instance.serial

    matching_orders = Order.objects.filter(robot_serial=robot_serial)

    if matching_orders:
        for order in matching_orders:
            customer = order.customer
            subject = 'Робот модели {} версии {} в наличии'.format(robot_model, robot_version)
            message = (
                'Добрый день!\n'
                'Недавно вы интересовались нашим роботом модели {}, версии {}. '
                'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'
            ).format(robot_model, robot_version)

            send_mail(subject, message, 'email@gmail.com', [customer.email])

            print("Отправлено уведомление клиенту:", customer.email)


post_save.connect(receiver=robot_created, sender=Robot)