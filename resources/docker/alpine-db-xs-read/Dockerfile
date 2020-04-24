FROM alpine:latest

RUN apk add sqlite

COPY common/sqlite/tpcc-xs.db /run/tpcc.db
COPY common/sqlite/read.sqlite /run/read.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh
RUN chmod +x /run/run.sh /usr/bin/sqlite3

CMD /run/run.sh /run/tpcc.db /run/read.sqlite
