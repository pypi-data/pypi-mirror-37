# tmpserver

v0.0.1

指定目录快速创建临时http服务，并显示url二维码



## install

```shell
pip install tmpserver
```

## usage

```
tmpserver -h 

usage: tmpserver [-h] [--bind ADDRESS] [--directory DIRECTORY] [--qr] [port]

positional arguments:
  port                  Specify alternate port [default: 8000]

optional arguments:
  -h, --help            show this help message and exit
  --bind ADDRESS, -b ADDRESS
                        Specify alternate bind address [default: all
                        interfaces]
  --directory DIRECTORY, -d DIRECTORY
                        Specify alternative directory [default:current
                        directory]
  --qr                  show qrcode in terminal
```


### example

```
(py3) ➜  tmpserver --qr -d /tmp/ 8899

█████████████████████████████████
█████████████████████████████████
████ ▄▄▄▄▄ █ ▄██▀ ▄ ▀█ ▄▄▄▄▄ ████
████ █   █ █▄█▀ ▀ ▀███ █   █ ████
████ █▄▄▄█ █▄▀ ▄▄  ▀██ █▄▄▄█ ████
████▄▄▄▄▄▄▄█▄▀ █▄▀ █▄█▄▄▄▄▄▄▄████
████ █▀▄▄▄▄ ▄▀██ █▀▄▄ ▀▀ ▀  ▄████
████▀▀█▄▄▄▄█ ▄██ ▀██▀██▀█ ▀▀ ████
████   ▀ ▀▄█ ▀▄▄▄  █▀ █  ██▀▄████
████ ▄▀ ▄▄▄ █▀█ ▄▄▀▀█▀ ▄ ▄ ▄ ████
████▄█▄███▄▄  ▄▀▀▀▄▄ ▄▄▄ ▄  █████
████ ▄▄▄▄▄ █  ▀▄▀█▀  █▄█ ▄ █ ████
████ █   █ █ ▄ █▄▄ █▄▄▄ ▄ █▄ ████
████ █▄▄▄█ ██▀ █▄█ █▄▀  ▀▀▄  ████
████▄▄▄▄▄▄▄█▄▄▄██▄▄█▄█▄█▄▄██▄████
█████████████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
Serving HTTP on 192.168.1.119 port 8899 with directory:/tmp/ (http://192.168.1.119:8899/) ...
```

## dependence
[qrcode](https://pypi.python.org/pypi/qrcode)