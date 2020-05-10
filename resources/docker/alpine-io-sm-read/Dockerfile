FROM alpine:latest

COPY common/io/sm /run/sm
COPY common/io/read.sh /run/read.sh
RUN chmod +x /run/read.sh

CMD /run/read.sh /run/sm
