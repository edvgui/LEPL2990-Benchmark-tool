FROM alpine:latest

RUN apk update \
	&& apk upgrade \
    && apk add sqlite

COPY common/sqlite/tpcc-sm.db /run/tpcc.db
COPY common/sqlite/read.sqlite /run/read.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh
RUN chmod +x /run/run.sh

CMD /run/run.sh /run/tpcc.db /run/read.sqlite
