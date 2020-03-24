# Read on sqlite database
Create a container that contains a big database and performs a large amount of read operations on it.

#### Build
```shell script
# From within this directory
docker build -t alpine-mondial-read -f Dockerfile ../../../

# From anywhere else
docker build -t alpine-mondial-read -f path/to/mondial-read/Dockerfile path/to/mondial-read/../../..
```

#### Launch
```shell script
docker run --rm alpine-mondial-read
```