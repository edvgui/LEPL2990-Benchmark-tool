FROM centos:7

COPY common/io/xl /run/xl
COPY common/io/read.sh /run/read.sh
RUN chmod +x /run/read.sh

CMD /run/read.sh /run/xl
