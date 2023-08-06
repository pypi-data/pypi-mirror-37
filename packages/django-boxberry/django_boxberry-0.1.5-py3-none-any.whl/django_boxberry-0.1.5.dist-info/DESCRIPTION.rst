Django-приложение для работы с Boxberry API
===========================================

*сделано с использованием*\ `python клиента
Boxberry <https://github.com/AlekseevAV/boxberry>`__

Установка
---------

Установить:

::

   pip install django-boxberry

или из github:

::

   pip install git+https://github.com/AlekseevAV/django-boxberry.git

Добавить django_boxberry в INSTALLED_APPS

::

   INSTALLED_APPS = (
       ...
       'django_boxberry',
   )

Добавить настройки Boxberry API settings.py

::

   BOXBERRY_TOKEN = 'token'
   BOXBERRY_ENDPOINT = 'http://test.boxberry.de/json.php'

Выполнить миграции

::

   python manage.py migrate django_boxberry


