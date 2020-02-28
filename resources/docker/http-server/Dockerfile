FROM alpine:latest

RUN apk update \
	&& apk upgrade \
	&& apk add lighttpd \
	&& rm -rf /var/cash/apk/* \
	&& echo "Hello World" > /var/www/localhost/htdocs/index.html
