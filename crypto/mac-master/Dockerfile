FROM redpwn/jail:0.1.3
COPY --from=python:3.10-slim-buster / /srv
COPY server.py /srv/app/run
COPY flag.txt /srv/app/

ENV JAIL_MEM=20M
