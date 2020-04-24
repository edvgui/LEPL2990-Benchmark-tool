FROM centos:7

RUN yum -y install glibc.i686 zlib.i686 \
    && rm -rf /usr/bin/sqlite3

COPY common/sqlite/sqlite3 /usr/bin/sqlite3
COPY common/sqlite/tpcc-sm.db /run/tpcc.db
COPY common/sqlite/read.sqlite /run/read.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh

RUN chmod +x /run/run.sh

CMD /run/run.sh /run/tpcc.db /run/read.sqlite
