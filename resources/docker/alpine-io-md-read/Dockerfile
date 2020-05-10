FROM alpine:latest

COPY common/io/md /run/md
COPY common/io/read.sh /run/read.sh
RUN chmod +x /run/read.sh

CMD /run/read.sh /run/md
