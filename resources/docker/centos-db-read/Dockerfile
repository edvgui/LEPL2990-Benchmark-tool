FROM centos:7

RUN yum -y install glibc.i686 zlib.i686

COPY common/sqlite/read.sqlite /run/read.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh

RUN chmod +x /run/run.sh

ARG size

COPY common/sqlite/tpcc-${size}.db /run/tpcc.db

CMD /run/run.sh /run/tpcc.db /run/read.sqlite
