"""
import patters here if they are in a different file.
"""


def debugprint(discr, exception):
    import inspect
    callerframerecord = inspect.stack()[1]

    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    filename = info.filename.split('/')[-1]
    fmt = (discr, info.function, filename, info.lineno, str(exception))
    print("%s %s in %s at: %s %s" % fmt)


"""#ohm led poles."""
# from PolicePattern import PolicePattern
# from BarberpolePattern import BarberpolePattern
# from ColorFadePattern import ColorFadePattern

"""
or ledmatrix
patterns that don't use pygame
"""

from RainPattern import *
from PixelLife import *
from Plasma import *
from sven import *
from LHC import * 

# uses pygame for testing.
try:
    from SuperPixelBros import SuperPixelBros
except Exception as e:
    debugprint("PixelBros >>", e)

# this one uses a library png so try to load.
# but if not installed pass.
try:
    from DisplayPng import *
except Exception as e:
    debugprint("DisplayPng >>", e)

# patterns that do use pygame
try:
    from Pong import *
except Exception as e:
    debugprint("Pong >>", e)

try:
    from Tron import *
except Exception as e:
    debugprint("Tron >>", e)

try:
    from Snake import *
except Exception as e:
    debugprint("snake >>", e)

# Graphics module has some tests in it too.
try:
    from Tools import *
except Exception as e:
    debugprint("graphics >>", e)
