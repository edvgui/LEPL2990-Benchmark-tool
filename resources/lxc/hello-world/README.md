# Hello world
Create a lxc container that prints a simple Hello World message in the console then quit.

#### Build

```shell script
./build.sh
```

#### Launch
```shell script
lxc launch -e alpine-hello-world a
lxc exec a -- /bin/echo Hello World
```