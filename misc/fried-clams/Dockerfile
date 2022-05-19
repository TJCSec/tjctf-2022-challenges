FROM redpwn/jail:0.1.3

# ubuntu:bionic-20220401
COPY --from=ubuntu@sha256:512274f1739676880585e70eea6a883db7b6d92841b02647b6c92b478356572c / /srv

# create bin/flag.txt with whatever inside
COPY bin/flag.txt /srv/app/
COPY bin/chall /srv/app/run
