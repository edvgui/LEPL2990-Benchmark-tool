FROM alpine:latest

COPY common/io/write.sh /run/write.sh
RUN chmod +x /run/write.sh

ARG size

COPY common/io/${size}.tar /run/source.tar

CMD /run/write.sh /run/source.tar /home
