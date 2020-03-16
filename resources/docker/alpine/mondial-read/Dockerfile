FROM alpine:latest

RUN apk add sqlite

RUN mkdir src
COPY common/sqlite/mondial-orig.db src/mondial-orig.db
COPY common/sqlite/read.sqlite src/read.sqlite
COPY common/sqlite/read.sh run.sh
RUN chmod +x run.sh

CMD /run.sh