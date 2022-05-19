FROM python:3.8-slim-buster AS app
RUN pip install --no-cache-dir pycryptodome

FROM redpwn/jail:0.1.3
COPY --from=app / /srv
COPY server.py /srv/app/run
COPY flag.txt /srv/app/

ENV JAIL_MEM=20M JAIL_TIME=600
