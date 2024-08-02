from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import EmailAccount, EmailMessage
from .serializers import EmailAccountSerializer, EmailMessageSerializer
from .services import fetch_emails

class EmailAccountViewSet(viewsets.ModelViewSet):
    queryset = EmailAccount.objects.all()
    serializer_class = EmailAccountSerializer

class EmailMessageViewSet(viewsets.ModelViewSet):
    queryset = EmailMessage.objects.all()
    serializer_class = EmailMessageSerializer

    def create(self, request, *args, **kwargs):
        email_account_id = request.data.get('email_account')
        for current, total, message in fetch_emails(email_account_id):
            progress = (current / total) * 100
            yield {
                "progress": progress,
                "message": {
                    "id": message.id,
                    "subject": message.subject,
                    "sent_date": message.sent_date,
                    "received_date": message.received_date,
                    "body": message.body[:100]  # Выводим только первые 100 символов текста
                }
            }
        return Response(status=201)

def message_list(request):
    return render(request, 'mail/messages.html')

def fetch_emails_view(request):
    email_account_id = request.GET.get('email_account_id')
    response_data = []
    for current, total, message in fetch_emails(email_account_id):
        response_data.append({
            "progress": (current / total) * 100,
            "message": {
                "id": message.id,
                "subject": message.subject,
                "sent_date": message.sent_date.isoformat(),
                "received_date": message.received_date.isoformat(),
                "body": message.body[:100]
            }
        })
    return JsonResponse(response_data, safe=False)
