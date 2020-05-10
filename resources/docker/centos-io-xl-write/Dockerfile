FROM centos:7

COPY common/io/xl.tar /run/xl.tar
COPY common/io/write.sh /run/write.sh
RUN chmod +x /run/write.sh

CMD /run/write.sh /run/xl.tar /home
