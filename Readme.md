# Mail Importer

Mail Importer - это веб-приложение, которое позволяет автоматически получать и отображать сообщения электронной почты из почтовых ящиков, используя Django, Django REST Framework, и Django Channels для реализации WebSocket-соединений. Приложение поддерживает работу с различными почтовыми сервисами и позволяет в реальном времени следить за процессом импорта сообщений.

## Функциональность

- Импорт сообщений из почтовых сервисов (например, Gmail) с использованием IMAP.
- Отображение списка сообщений в виде таблицы.
- Обновление прогресс-бара в реальном времени с использованием WebSocket.
- Декодирование и корректное отображение информации о сообщениях.
- Обработка и сохранение вложений из писем.
