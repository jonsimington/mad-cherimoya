# Instructions for execution
Since I couldn't be bothered to edit my PATH variable so that `python3` would work in git bash, I just copied and slightly edited `testRun` and `run` to call `python` instead of `python3`. These files are `testRunWindows` and `runWindows`. I left the originals untouched, so this will work everywhere now. 

# Note on board space text representation
The only weird thing about my submission is that I output spaces in a different way. I got annoyed with converting the string part of a (rank, file) coordinate system to an integer just to add things to it, so I use standard screen notation.
- `(0,0)` is the top-left corner of the board
- `(7, 7)` is the bottom-right corner of the board

I have updated the board printing function to reflect that

Every time the board prints, it now looks like this:

```  
   +------------------------+
 0 | r  n  b  q  k  b  n  r |
 1 | p  p  p  p  p  p  p  p |
 2 | .  .  .  .  .  .  .  . |
 3 | .  .  .  .  .  .  .  . |
 4 | .  .  .  .  .  .  .  . |
 5 | .  .  .  .  .  .  .  . |
 6 | P  P  P  P  P  P  P  P |
 7 | R  N  B  Q  K  B  N  R |
   +------------------------+
     0  1  2  3  4  5  6  7
```

This code was developed using PyCharm 2016.3.2 if that matters



# Chess Python 3 Client

This is the root of you AI. Stay out of the `joueur/` folder, it does most of the heavy lifting to play on our game servers. Your AI, and the game objects it manipulates are all in `games/chess/`, with your very own AI living in `games/chess/ai.py` for you to make smarter.

## How to Run

This client has been tested and confirmed to work on the Campus rc##xcs213 Linux machines, but it can work on your own Windows/Linux/Mac machines if you desire.

### Linux

```
./testRun MyOwnGameSession
```

For Linux, a recent version of `python3` should work. It has been tested on 3.4.3 extensively, but should work with >= 3.2. The normal 'python' usually refers to Python 2.7.X, so make sure you have the python**3** installed.

### Windows

On Windows you'll need some version of Python 3. As with the Linux version, [3.4.3][343] has been tested against extensively, however there's no none reason why it would not work on newer versions. Install that and ensure that python is set up in your Environmental Variables as 'python3', then

```
python3 main.py Chess -s r99acm.device.mst.edu -r MyOwnGameSession
```

## Make

There is a `Makefile` provided, but it is empty as python is an interpreted language. If you want to add `make` steps feel free to, but you may want to check with an Arena dev to ensure the Arena has the packages you need to use in `make`.

### Vagrant

Install [Vagrant][vagrant] and [Virtualbox][virtualbox] in order to use the Vagrant configuration we provide which satisfies all build dependencies inside of a virtual machine. This will allow for development with your favorite IDE or editor on your host machine while being able to run the client inside the virtual machine. Vagrant will automatically sync the changes you make into the virtual machine that it creates. In order to use vagrant **after installing the aforementioned requirements** simply run from the root of this client:

```bash
vagrant up
```

and after the build has completed you can ssh into the virtual environment by running:

```bash
vagrant ssh
```

From there you will be in a Linux environment that has all the dependencies you'll need to build and run this client.

When the competition is over, or the virtual environment becomes corrupted in some way, simply execute `vagrant destroy` to delete the virtual machine and its contents.

For a more in depth guide on using vagrant, take a look at [their guide][vagrant-guide]

#### Windows

Using Vagrant with Windows can be a bit of a pain. Here are some tips:

* Use an OpenSSH compatible ssh client. We recommend [Git Bash][gitbash] to serve double duty as your git client and ssh client
* Launch the terminal of your choice (like Git Bash) as an Administrator to ensure the symbolic links can be created when spinning up your Vagrant virtual machine

## Other Notes

It is possible that on your Missouri S&T S-Drive this client will not run properly. This is not a fault with the client, but rather the school's S-Drive implementation changing some file permissions during run time. We cannot control this. Instead, we recommend cloning your repo outside the S-Drive and use an SCP program like [WinSCP][winscp] to edit the files in Windows using whatever IDE you want if you want to code in Windows, but compile in Linux.

The only file you should ever modify to create your AI is the `ai.py` file. All the other files are needed for the game to work. In addition, you should never be creating your own instances of the Game's classes, nor should you ever try to modify their variables. Instead, treat the Game and its members as a read only structure that represents the game state on the game server. You interact with it by calling the game functions.

[343]: https://www.python.org/downloads/release/python-343/
[winscp]: https://winscp.net/eng/download.php
[vagrant]: https://www.vagrantup.com/downloads.html
[virtualbox]: https://www.virtualbox.org/wiki/Downloads
[vagrant-guide]: https://www.vagrantup.com/docs/getting-started/up.html
[virtualbox]: https://www.virtualbox.org/wiki/Downloads
[gitbash]: https://git-scm.com/downloads
