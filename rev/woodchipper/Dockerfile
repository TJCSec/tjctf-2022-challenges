FROM redpwn/jail:0.1.3
COPY --from=ubuntu:focal-20220113 / /srv
COPY bin/run bin/machine flag.txt prog.bin /srv/app/
