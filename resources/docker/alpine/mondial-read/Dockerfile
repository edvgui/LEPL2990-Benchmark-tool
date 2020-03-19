FROM alpine:latest

RUN apk update \
	&& apk upgrade \
    && apk add sqlite

COPY common/sqlite/mondial-orig.db /run/mondial-orig.db
COPY common/sqlite/read.sqlite /run/read.sqlite
COPY common/sqlite/sqlite.sh /run/run.sh
RUN chmod +x /run/run.sh

CMD /run/run.sh /run/mondial-orig.db /run/read.sqlite