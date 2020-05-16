FROM centos:7

COPY common/io/read.c /run/read.c
RUN yum install gcc -y \
    && gcc -o /run/read /run/read.c

ARG size

COPY common/io/$size /run/source

CMD /run/read /run/source
