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
    # mailing_list = Newsletters.objects.filter(date_next_mailing=now,
    #                                           state_mailing=[Newsletters.StateOfMailing.CREATED,
    #                                                          Newsletters.StateOfMailing.LAUNCHED],
    #                                           is_active=True)
    mailing_list = Newsletters.objects.all()
    for newsletter in mailing_list:
        subject_letter = newsletter.message.subject_letter
        text_letter = newsletter.message.text_letter
        clients_list = newsletter.clients.all()

        count_clients = len(clients_list)
        count_sent = 0

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
                count_sent += answer_server
            except smtplib.SMTPResponseException as error:
                # answer_server = str(error)
                pass

        mailing_report = create_report(newsletter, now, count_clients, count_sent)
        change_next_mailing_date_and_status(newsletter)
        status = change_status_logs(count_clients, count_clients)
        add_log_mailings(newsletter, data_send, status, mailing_report)


def change_status_logs(count_clients, count_sent):
    if count_clients == count_sent:
        return Logs.StatusOfLogs.SUCCESS
    elif count_sent == 0:
        return Logs.StatusOfLogs.FAILED
    else:
        return Logs.StatusOfLogs.PARTIALLY


def add_log_mailings(newsletter, date_last_mailing, status, mailing_report):
    Logs.objects.create(
        newsletter=newsletter,
        date_last_mailing=date_last_mailing,
        status_mailing=status,
        response_mail_server=mailing_report,
    )


def change_next_mailing_date_and_status(newsletter):
    periodicity = newsletter.frequency_mailing
    if periodicity == 'D':
        newsletter.date_next_mailing += timedelta(days=1)
    elif periodicity == 'W':
        newsletter.date_next_mailing += timedelta(days=7)
    elif periodicity == 'M':
        newsletter.date_next_mailing += timedelta(days=30)
    else:
        newsletter.date_next_mailing += timedelta(days=365)

    if newsletter.state_mailing == Newsletters.StateOfMailing.CREATED:
        newsletter.state_mailing = Newsletters.StateOfMailing.LAUNCHED

    newsletter.save()


def create_report(newsletter, now, count_clients, count_sent) -> str:
    report = (f'Рассылка "{newsletter.name_newsletter}" от {now.strftime('%d.%m.%Y %H:%M')} осуществлена. '
              f'Рассылка осуществлена {count_sent} клиентам из {count_clients}.')
    return report
