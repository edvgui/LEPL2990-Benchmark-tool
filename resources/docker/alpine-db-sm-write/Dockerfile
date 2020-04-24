FROM alpine:latest

COPY common/sqlite/sqlite3 /usr/bin/sqlite3
COPY common/sqlite/tpcc-sm.db /home/tpcc.db
COPY common/sqlite/write.sqlite /run/write.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh
RUN chmod +x /run/run.sh /usr/bin/sqlite3

CMD /run/run.sh /home/tpcc.db /run/write.sqlite