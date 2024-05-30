import logging
import smtplib
from datetime import datetime, timezone, timedelta
from django.core.mail import send_mail
from apps.newsletters.models import Newsletters, Logs
from config.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)


def start_mailing():
    """
    Функция осуществляющая рассылку сообщений по электронным почтам клиентов
    """
    now = datetime.now(timezone.utc)
    logger.info(now)
    # mailing_list = Newsletters.objects.filter(date_next_mailing=now, state_mailing=[Newsletters.StateOfMailing.CREATED,
    #                                                                                 Newsletters.StateOfMailing.LAUNCHED])
    mailing_list = Newsletters.objects.all()
    logger.info(mailing_list)
    for mailing in mailing_list:
        subject_letter = mailing.message.subject_letter
        text_letter = mailing.message.text_letter
        clients_list = mailing.clients.all()
        answer_server = None
        status = None
        for client in clients_list:
            data_send = datetime.now(timezone.utc)
            try:
                answer_server = send_mail(
                    subject=subject_letter,
                    message=text_letter,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )
                status = Logs.StatusOfLogs.SUCCESS
            except smtplib.SMTPResponseException as error:
                answer_server = str(error)
                status = Logs.StatusOfLogs.FAILED

            finally:
                add_log_mailings(mailing, data_send, status, answer_server)
        change_mailing_status(mailing)


def add_log_mailings(mailing, data_send, status, answer_server):
    Logs.objects.create(
        mailing=mailing,
        datatime=data_send,
        status=status,
        answer_mail_server=answer_server,
    )


def change_mailing_status(mailing):
    dict_periodicity = {
        'Ежедневно': 1,
        'Еженедельно': 7,
        'Ежемесячно': 30,
        'Ежегодно': 365
    }
    periodicity = dict_periodicity[mailing.periodicity]
    mailing_last = mailing.sent_time + timedelta(days=periodicity)
    if mailing_last > mailing.data_mailing_finish:
        mailing.status = mailing.StatusOfMailing.FINISHED
    else:
        mailing.sent_time = mailing_last
        mailing.status = mailing.StatusOfMailing.LAUNCHED

    mailing.save()
