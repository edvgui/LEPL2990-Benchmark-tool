FROM alpine:latest

RUN apk add sqlite

RUN mkdir src
COPY common/sqlite/mondial-orig.db src/mondial-orig.db
COPY common/sqlite/write.sqlite src/write.sqlite
COPY common/sqlite/write.sh run.sh
RUN chmod +x run.sh

CMD /run.sh