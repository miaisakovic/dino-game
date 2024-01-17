# T-Rex Dinosaur Game
A recreation of Google Chrome’s Dinosaur Game that can be played by showing your camera the palm of your hand. 

<p align="center">
  <img width="800" src="https://github.com/miaisakovic/dino-game/blob/main/images/dino_game.gif">
</p>

## Table of Contents
* [Setup](#setup)
  * [For Linux](#for-linux)
  * [For MacOS](#for-macos)
  * [After Installing Initial Requirements](#after-installing-initial-requirements)
* [How to Play](#how-to-play)

## Setup 
### For Linux
If Python has not been previously installed, run the following:
```
$ sudo apt install python3.9
$ python3.9 --version
```
If pip has not been previously installed, run the following:
```
$ sudo apt-get install python3-pip 
$ pip3 --version
```

### For MacOS
If Homebrew has not been previously installed, follow the instructions listed [here](https://brew.sh/).

If Python has not been previously installed, run the following:
```
$ brew install python@3.9
$ python3.9 --version
```
If pip has not been previously installed, run the following:
```
$ python3.9 -m ensurepip --upgrade
$ pip3 --version
```

### After Installing Initial Requirements
Clone this repository:
```
$ git clone https://github.com/miaisakovic/dino-game.git
``` 
When asked to enter credentials, input your username and personal access token.

Install the required dependencies included in requirements.txt:
```
$ pip3 install -r requirements.txt
```

## How to Play
Use the spacebar, or show your camera your open palm, to avoid colliding with the incoming obstacles or restart the game. 

Each time you would like to play this game, run the following command:
```
$ python3.9 <relative path to main.py>
```
