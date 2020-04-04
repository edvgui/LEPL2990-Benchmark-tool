# Read on sqlite database
Create a lxc container that contains a big database and performs a large amount of read operations on it.

#### Build
```shell script
./build.sh
```

#### Launch
```shell script
lxc launch -e alpine-db-read a
lxc exec a -- ./read.sh tpcc.db read.sqlite
```