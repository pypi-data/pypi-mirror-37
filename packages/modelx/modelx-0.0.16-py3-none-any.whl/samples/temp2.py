

import sys

def foo():
    sys.tracebacklimit = 0
    try:
        raise ValueError
    finally:
        del sys.tracebacklimit




