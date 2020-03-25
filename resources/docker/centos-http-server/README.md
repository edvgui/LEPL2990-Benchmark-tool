# Http server
Create a container that launches a lightweight http server.

#### Build
```shell script
# From within this directory
docker build -t centos-http-server .
```

#### Launch
```shell script
docker run --rm -d -p 127.0.0.1:3000:80 centos-http-server
```