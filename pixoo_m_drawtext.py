from os import getenv, stat, path
from time import sleep
from PIL import Image
import os, sys
from silkscreen.combine_letters import draw_text
from ifile import print_next_time

import modules.pixoo_client as pixc

if __name__ == "__main__":
    
    # pixoo max
    bt_mac_addr = '11:75:58:A2:B4:2D'
#    print(bt_mac_addr)
    
    pixoo = pixc.PixooMax(bt_mac_addr)
    connected = False
    
    lastfilepath=""
    thefilepath=""
    BRIGHTNESS=20
    while True:  # Main loop
        
        # first check if we're connected and connect if not
        if connected==False:
            try:
                pixoo.connect()
                connected=True
            except:
                print("Failed to open connection")
            
        if connected==True:
            # get next meeting time
            #timetext = ("doggy\nclub")
            soon = [0]
            timetext = print_next_time(soon)
            # TODO add countdown to start
            #print("next meeting at:",timetext)
            
            lastfilepath = thefilepath
            thefilepath = 'breaktime.png'
            if timetext != "":
                # make an image from the text
                draw_text(timetext)
                # that generates file 'tmp1.png' (white on black) and 'tmp2.png' (black on white)
                if soon[0] == False :
                    thefilepath = 'tmp1.png'
                else:
                    thefilepath = 'tmp2.png'
            
            noupdate = lastfilepath=='breaktime.png' and thefilepath=='breaktime.png'
            
            if not noupdate and path.exists(thefilepath):
                print("drawing "+thefilepath)
                try:
                    pixoo.draw_pic(thefilepath)
                except:
                    print("Failed to set image")
                    connected=False
            
            # while we're within 3 mins of a meeting make it visible by
            # cranking up the brightness
            if thefilepath == 'tmp2.png':
                BRIGHTNESS_CODE=0x0050
                pixoo.set_system_brightness(0x0000)
                pixoo.set_system_brightness(BRIGHTNESS_CODE)
            else:
                # pixoo has a habit of creeping brightness up when the cable is plugged into the device
                # (even if it's not plugged in at the other end).
                # either unplug it, or just keep setting the brightness to what we want
                
                # find out what brightness is desired
                # to maintain a system tray icon showing the current and desired brightness
                # we use a crappy hack of two files; the user clicking the system tray tool
                # updates the desired brightness file, but the displayed brightness is read
                # from a separate file that we only update when we actually change the pixoo brightness
                brightness_infile = "/home/marc/LinuxSystemFiles/pixoo-awesome/new_pixoo_m_brightness.txt"
                brightness_outfile = "/home/marc/LinuxSystemFiles/pixoo-awesome/pixoo_m_brightness.txt"
                # if new brightness request from user, update our BRIGHTNESS variable with its contents
                if(os.path.exists(brightness_infile)):
                    # open and get requeseted brightness
                    f = open(brightness_infile,"r+")
                    BRIGHTNESS_TEXT = f.read()
                    print("new brightness request: ",BRIGHTNESS_TEXT)
                    if(BRIGHTNESS_TEXT == ''): BRIGHTNESS_TEXT = str(BRIGHTNESS)
                    BRIGHTNESS = int(BRIGHTNESS_TEXT)
                    f.close()
                    os.remove(brightness_infile)
                    # update the current brightness file to update system tray icon with our new setting
                    f = open(brightness_outfile,"w+")
                    f.write(str(BRIGHTNESS))
                    f.close()
                # now apply the actual brightness change.
                # we always do this in every loop because, as mentioned, it can change on its own.
                if BRIGHTNESS < 10:
                    BRIGHTNESS_CODE=0x00ff
                elif BRIGHTNESS < 20:
                    BRIGHTNESS_CODE=0x000f
                elif BRIGHTNESS < 30:
                    BRIGHTNESS_CODE=0x0020
                elif BRIGHTNESS < 40:
                    BRIGHTNESS_CODE=0x0030
                elif BRIGHTNESS < 50:
                    BRIGHTNESS_CODE=0x0040
                elif BRIGHTNESS > 80:
                    BRIGHTNESS_CODE = 0x00f0
                else:
                    BRIGHTNESS_CODE=0x0050  # i can't be bothered to do them all.
                try:
                    # first set to off (possibly redundant)
                    pixoo.set_system_brightness(0x0000)
                    # set to fairly dim. keeps that whine quiet.
                    # can crank up to 0x0030-0x0050 for increasing brightness
                    pixoo.set_system_brightness(BRIGHTNESS_CODE)
                    #pixoo.set_system_brightness(0x0030)
                except:
                    print("failed to set brightness")
                    connected=False
        
        # sleep 60s
        sleep(60.0)
