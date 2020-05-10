FROM alpine:latest

COPY common/io/sm.tar /run/sm.tar
COPY common/io/write.sh /run/write.sh
RUN chmod +x /run/write.sh

CMD /run/write.sh /run/sm.tar /home
