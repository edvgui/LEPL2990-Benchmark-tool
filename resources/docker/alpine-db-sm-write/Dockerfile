FROM alpine:latest

RUN apk update \
	&& apk upgrade \
    && apk add sqlite

COPY common/sqlite/tpcc-sm.db /home/tpcc.db
COPY common/sqlite/write.sqlite /run/write.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh
RUN chmod +x /run/run.sh

CMD /run/run.sh /home/tpcc.db /run/write.sqlite
