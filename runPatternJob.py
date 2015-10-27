#!/usr/bin/env python
import socket
import signal
import sys
import imp
import os
import time
import collections
from matrix import matrix_width, matrix_height

loopPatterns = True


def get_trace():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    fmt = (exc_type, fname, exc_tb.tb_lineno)
    fmtstr = "%s:%s:%s" % fmt
    return fmtstr


def find_patterns_in_dir(dir):
    patterns = []
    # get the current working directory so we.
    # can join and find it.
    dir = os.path.join(os.getcwd(), dir)
    # see if dir is already in path. else add it.
    if dir not in sys.path:
        sys.path.append(dir)
    else:
        print("directory in path.")
    # for everything in a directory.
    for item in os.listdir(dir):
        # if it is a source file.
        if item.endswith("py"):
            # extract the file name and import it.
            sfile = item.split('.')[0]
            try:
                mod = __import__(sfile)
            except Exception as e:
                print("%s:Couldn't import module cause: %s" % (sfile, e))
                continue
            # extract classes
            classes = get_pattern_classes(mod)
            # if any found:
            if classes:
                # append the object to patterns
                patterns += classes
    # return the patterns
    return list(set(patterns))


def get_pattern_classes(module):
    # holds the patterns that are found
    patterns = []
    # look into the modules dictionary for the things in there
    for obj in module.__dict__:
        # if we find objects
        if isinstance(obj, object):
            try:
                # we try and get that objects dictionary.
                # if it's a class it will contain methods and more.
                thedict = module.__dict__[obj].__dict__
                # and if it contains the 'generate' method
                if(thedict['generate']):
                    # the class is appended to the list.
                    patterns.append(module.__dict__[obj])
            except:
                # continue if we try and read something we can't.
                continue
    # return a list of classes that have a generate function in them
    return patterns


def tst_patterns(dir, showpass=True):
    from matrix import matrix_size
    patterns = find_patterns_in_dir(dir)
    for pat in patterns:
        try:
            pattern = pat()
            generate = len(pattern.generate())
            if generate != matrix_size:
                raise Exception("%s:len of generated: %s" % (pat, generate))
            elif showpass:
                print("-----------------")
                print("passed: %s" % pat)
                print("-----------------")
        except Exception as e:
            print("---------------------")
            print("Pattern:%s Exception:%s" % (pat, e))
            print("---------------------")
            continue


def load_targets(configfile):
    # this function allows loading of the config files specified by
    # --config/configfile and load patterns defined in there.
    package = "configs"
    fp, path, description = imp.find_module(package)
    path = [path]
    fp, path, description = imp.find_module(str(configfile)[:-3], path)
    config = imp.load_module("configuration", fp, path, description)
    return config.TARGETS


def signal_handler(error, frame):
    # global loopPatterns
    # if error.code == 2:
    #     loopPatterns = False
    # else:
    print("\nExiting closing connections.")
    sock.close()
    sys.exit(0)


def debugprint(data):
    """Function that prints into the stdout, in the shape of the matrix."""
    from matrix import matrix_size, matrix_width
    chunksize = matrix_width
    for i in range(0, matrix_size, chunksize):
        print(data[i:i + chunksize])
    print("")


def checkList(first, second):
    for item1, item2 in zip(first, second):
        if item1 != item2:
            return False
    return True


def sendout(args):
    # sendout function that sends out data to the networked devices and
    # also to the matrix screen simulator if enabled.
    # or only to the matrix simulator if netSilent enabled.
    try:
        for t in TARGETS:
            pattern = TARGETS[t]
            data = pattern.generate()
            # make sure matrixSim always displays
            # the data the right way.
            # can't have the matrixsimulator hang because there is not change..
            if args.matrixSim == "enabled":
                matrixscreen.handleinput()
            # if this is a simulation draw it to the matrixscreen
            if args.matrixSim == "enabled":
                    matrixscreen.process(data)
            # convert the data for the special matrix layout.
            if args.snakeMode == "enabled":
                data = convertSnakeModes(data)
            if args.byteMode == "enabled":
                data = convertByteMode(data, args.convertColor)
            # check if data generated is the same as before because then
            # just don't send it out
            change = True
            if args.soc == "enabled":
                previous_set = collections.Counter(sendout.data)
                current_set = collections.Counter(data)
                change = previous_set != current_set
            elif args.soc == "disabled":
                change = True
            if(change):
                sendout.data = data
                # send it out over the network.
                if not (args.netSilent == "enabled"):
                    try:
                        if (args.mapy == "enabled"): 
                            for universe in range(0,matrix_height-1):
                                sock.sendto(buildPacket(universe, data[matrix_width*universe:(matrix_width*universe)+(matrix_width)]), (t, UDP_PORT))    
                        else:
                            #sock.sendto(buildPacket(0, data), (t, UDP_PORT))
                            #sock.sendto(buildPacket(1, data), (t, UDP_PORT))
                            #sock.sendto(buildPacket(2, data), (t, UDP_PORT))
                            sock.sendto(buildPacket(3, data), (t, UDP_PORT))
                            #sock.sendto(buildPacket(4, data), (t, UDP_PORT))
                            #sock.sendto(buildPacket(5, data), (t, UDP_PORT))
                    except Exception:
                        print("no good ip dest found: %s" % (t))
                        sys.exit(0)
    # matrix sim needs this because i am to lazy to press the x button.
    except KeyboardInterrupt:
        signal_handler(None, None)
    except SystemExit as error:
        signal_handler(error, None)
sendout.data = []


def listpatterns():
    patterns = find_patterns_in_dir('patterns')
    for pat in patterns:
        print(pat.__name__)


if __name__ == "__main__":
    from ArgumentParser import get_args
    # get command line arguments:
    args = get_args()
    if args.list:
        listpatterns()
        sys.exit()
    if args.testing:
        tst_patterns('patterns', showpass=False)
        print("Done testing. ")
        sys.exit()
    # if gui selected start that else start the headless code.
    if args.gui == "enabled":
        try:
            from Gui.Gui import Gui
            editor = Gui(args)
            editor.main()
        except Exception as e:
            print(e)
        print("Exiting.")
        sys.exit(0)
    else:
        from artnet import buildPacket
        from matrix import matrix_width, matrix_height
        from matrix import convertSnakeModes, convertByteMode
        from MatrixSim.MatrixScreen import interface_opts
        try:
            from MatrixSim.MatrixScreen import MatrixScreen
        except Exception as e:
            print("MatrixScreen>> " + str(e))

        UDP_PORT = 6454
        TARGETS = load_targets(args.config)

        # check if there is anything configured.
        if not len(TARGETS):
            print("nothing is configured in %s" % args.config)
            sys.exit(1)
        # ---------

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        signal.signal(signal.SIGINT, signal_handler)

        # setup a screen if matrixSim argument was set.
        if args.matrixSim == "enabled":
            if args.fullscreen == "enabled":
                fullscreen = True
            else:
                fullscreen = False
            interface = interface_opts[args.simInterface]
            matrixscreen = MatrixScreen(matrix_width, matrix_height,
                                        args.pixelSize,
                                        fullscreen,
                                        interface)

        if args.fps > 0:
            fps = 1. / args.fps

        previousTime = time.time()
        while(True):
            #os.system('read -s -n 1 -p "Press any key to continue..."')
            loopPatterns = True
            while(loopPatterns):
                # send patterns out in a timed fasion. if args.fps != 0
                if args.fps > 0:
                    sendout(args)
                    # TODO: figure out how to dynamicly
                    # adjust time as to have a fixed fps.
                    time.sleep(fps)
                # else send everything out as fast as possible
                else:
                    sendout(args)
            time.sleep(0.5)
        signal_handler(None, None)
