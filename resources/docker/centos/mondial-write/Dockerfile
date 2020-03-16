FROM centos:7

RUN yum -y install glibc.i686 zlib.i686

RUN mv /usr/bin/sqlite3 /usr/bin/sqlite3.7
COPY common/sqlite/sqlite3 usr/bin/sqlite3

RUN mkdir src
COPY common/sqlite/mondial-orig.db src/mondial-orig.db
COPY common/sqlite/write.sqlite src/write.sqlite
COPY common/sqlite/write.sh run.sh
RUN chmod +x run.sh

CMD /run.sh