FROM centos:7

COPY common/io/xs /run/xs
COPY common/io/read.sh /run/read.sh
RUN chmod +x /run/read.sh

CMD /run/read.sh /run/xs
