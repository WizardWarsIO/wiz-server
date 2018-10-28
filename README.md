[http://WizardWars.IO](http://WizardWars.IO)
A Roguelike Deathmatch. 

WizardWars.io is a turn-based combat game running on a 1-second clock.

Game logic/server written in Python. Uses Libtcod and Flask. Client uses React.js.

![Screenshot](screenshot.png?raw=true "Screenshot")

[1:26 Player Tutorial Video](https://www.youtube.com/watch?v=An9qhpav9kM)

[58:58 Code Overview Video](https://www.youtube.com/watch?v=WU-UTHbe3Hc)
```
$ pip install flask
$ pip install flask_socket
$ pip install socketIO_client
$ pip install gevent
```

Follow the instructions for libtcod from [https://github.com/libtcod/python-tcod#linux](https://github.com/libtcod/python-tcod#linux)

```
$ sudo apt-get install gcc python-dev python3-dev libsdl2-dev libffi-dev libomp5
$ pip2 install tcod
$ pip3 install tcod
```

Start the server + turn timer:

```
$ cd wizard-wars
$ screen -S server
$ ./run.sh
ctrl+A,D
$ screen -S socket
$ python socketclient.py
$ ./run.sh
ctrl+A,D
```

Written by R. Riley Holmes and Quantum Potato, May-October 2018
