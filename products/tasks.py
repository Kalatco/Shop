from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.utils.log import get_task_logger
from django.template.loader import render_to_string

logger = get_task_logger(__name__)

@shared_task
def send_order_email(orderSerializer, orderItemsList, totalCost):

    email_template = render_to_string('order.txt',
        {
            'firstName': orderSerializer['customer']['first_name'],
            'lastName': orderSerializer['customer']['last_name'],
            'products': orderItemsList,
            'totalCost': totalCost
        })
    logger.info(email_template)

    subject = 'New order created'
    email_to = [orderSerializer['customer']['email']]
    email_from = settings.EMAIL_HOST_USER
    return send_mail(subject, email_template, email_from, settings.EMAIL_RECIPIENTS)
