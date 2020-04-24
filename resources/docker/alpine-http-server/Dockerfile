FROM alpine:latest

RUN apk add lighttpd \
	&& rm -rf /var/cash/apk/* \
	&& echo "Hello World" > /var/www/localhost/htdocs/index.html \
	&& sed -i 's/server.username      = "lighttpd"/# server.username      = "lighttpd"/g' /etc/lighttpd/lighttpd.conf \
	&& sed -i 's/server.groupname     = "lighttpd"/# server.groupname     = "lighttpd"/g' /etc/lighttpd/lighttpd.conf

CMD /usr/sbin/lighttpd -D -f /etc/lighttpd/lighttpd.conf
