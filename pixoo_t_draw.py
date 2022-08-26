from os import getenv, stat, path
from time import sleep
from PIL import Image

import modules.pixoo_client as pixc

if __name__ == "__main__":
    # pixoo max
    bt_mac_addr = '11:75:58:1E:A9:52'
    
#    print(bt_mac_addr)
    pixoo = pixc.Pixoo(bt_mac_addr)
    pixoo.connect()
    
    cached_stamp=0
    stamp = 0
    if path.exists('/tmp/plot.bmp'):
        # check last modified time
        stamp = stat('/tmp/plot.bmp').st_mtime
    while True:  # Main loop
        if path.exists('/tmp/plot.bmp'):
            stamp = stat('/tmp/plot.bmp').st_mtime
        if stamp != cached_stamp:
            cached_stamp = stamp
            pixoo.draw_pic("/tmp/plot.bmp")
        sleep(1.0)

