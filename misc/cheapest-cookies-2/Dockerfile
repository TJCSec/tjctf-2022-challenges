FROM python:3.10-slim-buster AS app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM redpwn/jail:0.1.3

COPY --from=app / /srv
COPY server.py /srv/app/run
COPY flag.txt /srv/app/

ENV JAIL_MEM=20M
