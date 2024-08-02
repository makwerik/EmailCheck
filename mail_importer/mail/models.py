from django.db import models


# Create your models here.
class EmailAccount(models.Model):
    """Храним данные от почты"""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email



class EmailMessage(models.Model):
    """Храним сообщения"""
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()
    attachments = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.subject