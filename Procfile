release: python manage.py migrate
web: gunicorn review_tracker.wsgi
celery: celery -A review_tracker.celery worker --concurrency 1 -l info
