FROM centos:7

COPY common/io/md.tar /run/md.tar
COPY common/io/write.sh /run/write.sh
RUN chmod +x /run/write.sh

CMD /run/write.sh /run/md.tar /home
