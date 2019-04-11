FROM python:3.7-alpine

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH /app
CMD ["gunicorn", "--threads", "10", "-w", "1", "-b", "0.0.0.0:8000", "-k", "gthread", "server:app"]