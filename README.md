[![Build Status](https://travis-ci.org/TkkrLab/py-artnet.svg?branch=master)](https://travis-ci.org/TkkrLab/py-artnet)
py-art-net
==========

Python art net interface. with patterns you can run for the ledpoles and the ledmatrix fridgefire made.

or anything that has a network based artnet interface.

I made it easier to config and run patterns with python code.


#### Dependencies.
* python2.7	[source](https://www.python.org/downloads/)
* pypng		[source](https://pypi.python.org/pypi/pypng)
* pygame	[source](http://pygame.org/news.html)
* pyserial-2.7	[source](https://pypi.python.org/pypi/pyserial)
* pygtk 	[source](http://www.pygtk.org/downloads.html)
* pygtksourveiw2[source](http://packages.ubuntu.com/lucid-updates/python/python-gtksourceview2)
* PyOpenGl	[source](https://pypi.python.org/pypi/PyOpenGL)
* SciPy     [source](http://www.scipy.org/)
* NumPy     [source](http://www.numpy.org/)
* PyAudio   [source](http://people.csail.mit.edu/hubert/pyaudio/)
* alsaseq [source](http://pp.com.mx/python/alsaseq/)
* alsaaudio [source](http://pyalsaaudio.sourceforge.net/)

#### what to do if you want to run it ?

make you pattern, import it into patterns.py

then in configs folder created a config file or edit a existing one.

create it like:

name_conf.py

use a existing config as a template and follow it.

you can run multiple devices from a signle config file.

as wel as multpile patterns like:


```python
    TARGETS {
        target1_ip:pattern(),
        target2_ip:nextPattern(),
        target3_ip:anotherPattern(),
    }
```

Then to run the actual patterns you run from the command line:

```shell
    :$ python runPatternJob.py --fps=<fps> --config=<config>
```

for example:

```shell
    :$ python runpatternJob.py --fps=25 --config=myLamps_conf.py
```

both fps and config are optional,

the default framerate is 15 Fps which is the delay that dictates how fast the refresh is ran, or packets are sendout.

and the default config is default_conf.py

which won't work if you didn't put the right things in it. like the right ip.

etc etc.

if you want to run the code with the build in simulator just add --matrixSim=enabled

to the command line options and it will run localy on your screen.

for example:
```shell
    :$ python runpatternJob.py --fps=25 --config=myLamps_conf.py --matrixSim=enabled
```


but ofcourse this wouldn't look right if you config file contains code for anything other than a matrix display.

but you can view the display as a string of pixels though, cause basicly in reality it is just that.


# this software is used in a pixel matrix project:
[PixelMatrix with artnet interface](https://www.tkkrlab.nl/wiki/Pixelmatrix)

# Art-Editor
## how to run the editor forexample:
```shell
    robert@Laptop:~/py-artnet$ python runPatternJob.py --gui=enabled
```

what if you see a message like:
'''shell
    /usr/lib/python2.7/dist-packages/gtk-2.0/gtk/__init__.py:57: GtkWarning: could not open display warnings.warn(str(e), _gtk.Warning)
'''

that meens your version of pygtk is to old. you are required to have a version installed thats above 2.0

## Hard to find docs hu.
http://soc.if.usp.br/manual/python-gtksourceview2/html/

## ideas
* been working on a gui/editor to make patterns on the go, which features live code reloading, and a build in simulator
* need to put downs some ideas soon like a line number ruler thing and indentation follow.[line numbers implemented, syntaxhighlighting implemented, indentation follow implemented]
* and more things like that.
* create a few editeable settings like fps. and maybe a a live mode (sending out udp artnet to devices)
* find ways to discover devices and display.
* put some diagnostic output under the matrix simulator. [partialy implemented]

## the editor supports:
* auto indentation follows indentation level.
* indentation after a : and unindent after break pass return continue.
* basicly ported this to my code: http://osdir.com/ml/gnome.apps.gedit/2008-06/msg00027.html
* it has syntax highlighting.
* dynamic reloading triggerd on key-releases.
* dynamic looking for generate function (has to be inside a class)
* indenting in spaces, where spaces are show as spaces with dots in them to show the level
* has some action that can be performed through the menu.
* you can open files save them in a tempfile names new_file.py (Control - O, Control-S)
* reload code with Control-R and menu item
* Control-Q or quit through menu.
* undo changes (Control-Z)
* redo changes (Control-Y)
* output for easy showing where errors are and what kind of errors are/were generated. (under the simulator)

#### usefull tools:
compile:

[artnet-c](https://github.com/ohm2013loc/art)

run:

artmonitor <ip>     #tells a bit more info on the device like mac address and more.

artpoll <broadcast>     #finds all the devices on the network. writes that data to a file. make sure field-devices exist (file)

artdmxtest <ip>     #runs a fading pattern, usefull for testing if the art-net device works.



#### on the todo list:

* FallingStars [it is broken it worked it was done and now it doesn't even run. only half the code is there. probably a commit thing happend.]

* implentation of pixelbros [W.I.P]

* pong [Done]

* snake [Done]

* tron [W.I.P]

* tetris 

* arcadia

* game of life (conway) [Done it's called PixelLife]

* VU meter [partialy done, have a effect running]

* network monitor 

* make mario appear on the matrix or other mobs from the game or any other image from other games.

* problem with pwm not being linear (the amount of power it gives per pulse)

thus implement a scale which does make it linear. so fading is nice and even.

* link that gave me the Yes that's it! moment:
* http://forum.arduino.cc/index.php?PHPSESSID=fiq8nr1j9sstegstf2o6btdgq2&topic=286351.0

* break out patterns in patterns.py in to seperate files. [done]

* I think it would be helpfull to implement a "Graphics" library [This is done the class is called Graphics]

also implemented a color library, and classes for making color objects. handy for pallets and much more.

#### other things that might be verry usefull to make or do:
more a hardware todo is make firmware for the ESP8266 wifi module
that does artnet. no need for utp cables any more. [W.I.P ()]
for example this [video](https://youtu.be/BJuSRD35P3M) is what i have been working on.

