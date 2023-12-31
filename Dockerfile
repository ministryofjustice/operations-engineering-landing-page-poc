FROM python:3.11.5-slim

RUN addgroup --gid 1017 --system appgroup \
  && adduser --system --uid 1017 --group appgroup

RUN apt update -y && apt dist-upgrade -y && apt install -y

WORKDIR /home/operations-engineering-poc-landing-page

COPY requirements.txt requirements.txt
COPY landing_page_app landing_page_app
COPY operations_engineering_landing_page.py operations_engineering_landing_page.py

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

USER 1017

EXPOSE 4567

CMD ["gunicorn", "--bind=0.0.0.0:4567", "operations_engineering_landing_page:app()"]
