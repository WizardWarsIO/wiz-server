[http://WizardWars.IO](http://WizardWars.IO)
A Roguelike Deathmatch. 

WizardWars.io is a turn-based combat game running on a 1-second clock.

Game logic/server written in Python. Uses Libtcod and Flask. Client uses React.js.

![Screenshot](screenshot.png?raw=true "Screenshot")

[1:26 Player Tutorial Video](https://www.youtube.com/watch?v=An9qhpav9kM)

[58:58 Code Overview Video](https://www.youtube.com/watch?v=WU-UTHbe3Hc)




## (Optional but recommended) Use a virtual environment
For more informations on `virtualenv`, check its [documentation](https://virtualenv.pypa.io/en/latest/).

Start by creating a virtual environment folder.
```
$ virtualenv env
```
A good place for it is next to the repository folder.
```
.
├── env/
└── wiz-server/
```
Make sure to use python 2, this can be achieved with the `--python` option like so :
```
$ virtualenv --python=/usr/bin/python2.7 env
```
Finally, you have to "activate" the environment by sourcing `env/bin/activate`.
```
$ source env/bin/activate
(env) $
```
The prompt should change to indicate the current virtual environment.

## Install tcod dependencies
The `tcod` package requires some additionnal dependencies. See the [tcod installation instructions](https://github.com/libtcod/python-tcod#installation).


## Install Python dependencies
The dependencies are listed in `requirements.txt`, to install them, just run
```
$ pip install -r requirements.txt
```





## Start the server + turn timer:

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
