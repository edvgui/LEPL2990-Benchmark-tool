FROM alpine:latest

RUN apk add sqlite

COPY common/sqlite/tpcc-lg.db /home/tpcc.db
COPY common/sqlite/write.sqlite /run/write.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh
RUN chmod +x /run/run.sh /usr/bin/sqlite3

CMD /run/run.sh /home/tpcc.db /run/write.sqlite