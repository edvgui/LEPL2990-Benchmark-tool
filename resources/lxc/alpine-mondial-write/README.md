# Write on sqlite database
Create a lxc container that contains a big database and performs a large amount of write operations on it.

#### Build
```shell script
./build.sh
```

#### Launch
```shell script
lxc launch -e alpine-mondial-write a
lxc exec a -- ./write.sh
```