import os
import sys
def log(msg=None, level='INFO'):
    pfx = 'ProtonFixes[' + str(os.getpid()) + '] '+ level +': '
    sys.stderr.write(pfx + str(msg) + os.linesep)
    sys.stderr.flush()