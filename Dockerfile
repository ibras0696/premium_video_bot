FROM ubuntu:latest
LABEL authors="chupi"

ENTRYPOINT ["top", "-b"]