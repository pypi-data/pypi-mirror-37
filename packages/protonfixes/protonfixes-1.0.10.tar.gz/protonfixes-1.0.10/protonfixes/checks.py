""" Run some tests and generate warnings for proton configuration issues
"""

from .logger import log

ESYNC_WARNING = ''' File descriptor limit is low
This can cause issues with ESYNC
For more details see:
https://github.com/zfigura/wine/blob/esync/README.esync
'''

# https://www.reddit.com/r/SteamPlay/comments/9kqisk/tip_for_those_using_proton_no_esync1/
#/proc/sys/fs/file-max
def esync_file_limits():
    with open('/proc/sys/fs/file-max') as fsmax:
        max_files = fsmax.readline()
        if int(max_files) < 8192:
            log.warn(ESYNC_WARNING)

esync_file_limits()
