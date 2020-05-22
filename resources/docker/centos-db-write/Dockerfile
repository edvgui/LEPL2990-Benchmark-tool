FROM centos:7

RUN yum -y install glibc.i686 zlib.i686

COPY common/sqlite/write.sqlite /run/write.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh

RUN chmod +x /run/run.sh

ARG size

COPY common/sqlite/tpcc-${size}.db /home/tpcc.db

CMD /run/run.sh /home/tpcc.db /run/write.sqlite
