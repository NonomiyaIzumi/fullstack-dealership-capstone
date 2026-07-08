FROM python:3.12-slim

WORKDIR /app

ENV DJANGO_DEBUG=False

COPY pyproject.toml ./
RUN pip install --no-cache-dir django requests whitenoise gunicorn

COPY . .

RUN python manage.py collectstatic --noinput
RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
