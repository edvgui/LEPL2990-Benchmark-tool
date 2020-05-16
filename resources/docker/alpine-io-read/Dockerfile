FROM alpine:latest

COPY common/io/read.c /run/read.c
RUN apk add build-base \
    && gcc -o /run/read /run/read.c

ARG size

COPY common/io/$size /run/source

CMD /run/read /run/source
