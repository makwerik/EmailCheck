import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import fetch_emails

class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        email_account_id = self.scope['url_route']['kwargs'].get('email_account_id', 1)
        async for progress, message in fetch_emails(email_account_id):
            await self.send(json.dumps({
                'progress': progress,
                'message': {
                    'id': message.id,
                    'subject': message.subject,
                    'sent_date': message.sent_date.isoformat(),
                    'received_date': message.received_date.isoformat(),
                    'body': message.body[:100]  # Краткое содержание
                }
            }))

    async def disconnect(self, close_code):
        pass
