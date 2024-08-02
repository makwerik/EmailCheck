import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import os
from django.conf import settings
from .models import EmailAccount, EmailMessage


def decode_mime_words(s):
    return ''.join(
        word.decode(encoding or 'utf-8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s)
    )


def fetch_emails(email_account_id):
    # Получаем учетную запись электронной почты из базы данных
    email_account = EmailAccount.objects.get(id=email_account_id)

    # Подключение к почтовому серверу
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_account.email, email_account.password)
    mail.select("inbox")

    # Поиск всех писем в почтовом ящике
    _, search_data = mail.search(None, 'ALL')
    message_ids = search_data[0].split()
    total_messages = len(message_ids)

    for index, num in enumerate(message_ids):
        _, data = mail.fetch(num, '(RFC822)')
        _, bytes_data = data[0]

        # Преобразование письма в объект email.message
        msg = email.message_from_bytes(bytes_data)

        # Декодирование темы письма
        subject = decode_mime_words(msg["subject"])

        # Извлечение даты отправки
        sent_date = parsedate_to_datetime(msg["Date"])

        # Извлечение текста письма
        body = ""
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Если это вложение, сохраняем его
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = decode_mime_words(filename)
                        filepath = os.path.join(settings.MEDIA_ROOT, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        attachments.append(filepath)
                elif content_type == "text/plain" and not body:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

        # Сохраняем каждое сообщение в базу данных
        message = EmailMessage.objects.create(
            email_account=email_account,
            subject=subject,
            sent_date=sent_date,
            received_date=sent_date,
            body=body,
            attachments=attachments
        )

        # Возвращаем прогресс
        yield (index + 1) / total_messages * 100, message

    mail.logout()
