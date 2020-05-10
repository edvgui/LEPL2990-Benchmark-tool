FROM centos:7

COPY common/io/lg.tar /run/lg.tar
COPY common/io/write.sh /run/write.sh
RUN chmod +x /run/write.sh

CMD /run/write.sh /run/lg.tar /home
