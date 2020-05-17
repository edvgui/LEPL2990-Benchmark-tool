# Ping
Create a lxc container that performs a few ping requests and prints the final result.

#### Build
```shell script
./build.sh
```

#### Launch
```shell script
lxc launch -e alpine-network a
lxc exec a -- ./ping.sh
```