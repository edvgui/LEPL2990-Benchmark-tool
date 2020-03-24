# Http server
Create a container that prints a simple Hello World message in the console then quit.

#### Build
```shell script
# From within this directory
docker build -t alpine-http-server .
```

#### Launch
```shell script
docker run --rm -d -p 127.0.0.1:3000:80 alpine-http-server 
```