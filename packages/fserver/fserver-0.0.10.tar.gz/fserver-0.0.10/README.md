# fserver
a simple http.server implement with flask and gevent


### install 
```shell
$ sudo pip install fserver
```


### usage
```
usage: fserver [-h] [-d] [--ip ADDRESS] [port]

  positional arguments:
    port                  Specify alternate port [default: 2000]

  optional arguments:
    -h, --help            show this help message and exit
    -d, --debug           use debug mode of fserver
    -i ADDRESS, --ip ADDRESS,
                          Specify alternate bind address [default: all interfaces]

  arguments of url:
    m                     get_arg to set the mode of processing method of file
                          Such as http://localhost:port?m=dv to download the file specified by url
                          value 'p' to play file with Dplayer
                          value 'v' to show the file specified by url
                          value 'dv' to download the file specified by url
```
### license
[MIT](LICENSE)