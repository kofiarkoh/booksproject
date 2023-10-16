from mail_templated import EmailMessage
from celery import shared_task

@shared_task()
def send_password_reset_otp():
    message = EmailMessage('mail/password_reset_otp.html',
                           {}, from_email='t@gmail.com', to=['u@gmail.com']
                           )
    message.content_subtype
    message.send()