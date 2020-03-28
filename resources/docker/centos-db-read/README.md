# Read on sqlite database
Create a container that contains a big database and performs a large amount of read operations on it.

#### Build
```shell script
# From within this directory
docker build -t centos-db-read -f Dockerfile ../../../

# From anywhere else
docker build -t centos-db-read -f path/to/mondial-read/Dockerfile path/to/mondial-read/../../..
```

#### Launch
```shell script
docker run --rm centos-db-read
```