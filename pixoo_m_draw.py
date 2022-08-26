from os import getenv, stat, path
from time import sleep
from PIL import Image
import os, sys

import modules.pixoo_client as pixc

if __name__ == "__main__":
    
    # pixoo max
    bt_mac_addr = '11:75:58:A2:B4:2D'
    
#    print(bt_mac_addr)
    pixoo = pixc.PixooMax(bt_mac_addr)
    pixoo.connect()
    
    cached_stamp=0
    stamp = 0
    if len(sys.argv) > 1:
        thefilepath = sys.argv[1]
    else:
        thefilepath = '/tmp/plot.bmp'
    
    if len(sys.argv) > 2:
        loop = sys.argv[2]
    else:
        loop = True
    
    if path.exists(thefilepath):
        # check last modified time
        stamp = stat(thefilepath).st_mtime
    while loop:  # Main loop
        if path.exists(thefilepath):
            stamp = stat(thefilepath).st_mtime
        if stamp != cached_stamp:
            cached_stamp = stamp
            print("drawing "+thefilepath)
            pixoo.draw_pic(thefilepath)
        sleep(1.0)
