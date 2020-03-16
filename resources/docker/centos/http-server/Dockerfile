FROM centos:7

RUN yum -y update \
	&& yum -y install epel-release \
	&& yum -y update \
	&& yum -y install lighttpd \
	&& rm -rf /var/cash/apk/* \
	&& echo "Hello World" > /var/www/lighttpd/index.html \
	&& sed -i 's/server.use-ipv6 = "enable"/server.use-ipv6 = "disable"/' /etc/lighttpd/lighttpd.conf

CMD /usr/sbin/lighttpd -D -f /etc/lighttpd/lighttpd.conf