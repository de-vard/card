# Почтовые отправления
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # хост SMTP-сервера
EMAIL_HOST_USER = 'krolik.zip23@gmail.com'  # логин пользователя для SMTP-сервера
EMAIL_HOST_PASSWORD = 'djztgaoyqawzmovc'  # пароль пользователя для SMTP-сервера
EMAIL_PORT = 587  # порт SMTP-сервера
EMAIL_USE_TLS = True  # использовать ли защищенное TLS-подключение
DEFAULT_FROM_EMAIL = 'МОЙ ДОМЕН<admin@mail.ru>'  # От кого будут отправляться письма
