1) start  daphne server for channels, it runs on 8002

python manage.py makemigrations
python manage.py migrate

STATIC_ROOT = '/yogasoft/static'    # in settings.py
STATIC_ROOT = '/yogasoft/media'    # in settings.py
python manage.py collectstatic

daphne -b 0.0.0.0 -p 8002 yogasoft.asgi:channel_layer
python manage.py runserver 0.0.0.0:8000


2) we need postgresql and redis to be installed
3) MANIFEST.in is used for package release
