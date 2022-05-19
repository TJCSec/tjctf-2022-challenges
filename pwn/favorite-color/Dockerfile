FROM redpwn/jail:0.1.3

COPY --from=ubuntu / /srv

WORKDIR /srv/app/

COPY bin/flag.txt .
COPY bin/chall run
