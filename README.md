[http://WizardWars.IO](http://WizardWars.IO)
A Roguelike Deathmatch. 

WizardWars.io is a turn-based combat game running on a 1-second clock.

Game logic/server written in Python. Uses Libtcod and Flask. Client uses React.js.

![Screenshot](screenshot.png?raw=true "Screenshot")

[90 Second Tutorial Video](https://www.youtube.com/watch?v=An9qhpav9kM)

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
