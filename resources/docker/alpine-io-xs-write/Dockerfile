FROM alpine:latest

COPY common/io/xs.tar /run/xs.tar
COPY common/io/write.sh /run/write.sh
RUN chmod +x /run/write.sh

CMD /run/write.sh /run/xs.tar /home
