# WikiNZ Hackfest

## Installation

```
git clone --recursive git@github.com:opcode/wikinz-hf

cd wikinz-hf

virtualenv -p python2.7 .
source bin/activate

trex/bin/install-deps.sh -d

cd app/
cp local.ini.dist local.ini
vim local.ini
```

## Running

You probably want to make sure you have the less-watcher running in a terminal

```
app watch_static
```

To run the site in debug-mode, simply:

```
app
```
