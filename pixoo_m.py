from os import getenv
from time import sleep
from PIL import Image
# for youtube
import subprocess
import json
import requests

import modules.pixoo_client as pixc

#load_dotenv("local.env", verbose=True)

if __name__ == "__main__":
    # pixoo max
    bt_mac_addr = '11:75:58:A2:B4:2D'
    
#    print(bt_mac_addr)
    pixoo = pixc.PixooMax(bt_mac_addr)
    pixoo.connect()
    
    print("drawing pic")
#    pixoo.draw_pic("/home/marc/Desktop/pomuglow.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/pomulol.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/pomuglow.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/pomulol.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/pomuglow.png")
#    sleep(1.0)

#    pixoo.draw_pic("/home/marc/Desktop/calliglow.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/deadbeats.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/calliglow2.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/deadbeats.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/calliglow.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/deadbeats.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/calliglow2.png")
#    sleep(1.0)
    pixoo.draw_pic("/home/marc/Desktop/callismile2.png")
#    sleep(1.0)
#    pixoo.draw_pic("/home/marc/Desktop/calliblk.png")
#    pixoo.set_system_brightness(0x000)
#    pixoo.set_system_brightness(0x0030)
    # 0x000, then 0x00ff - most dim...
    # 0x000, then 0x000f - slightly less dim... but still very dim
    # 0x000, then 0x00f0 - very bright (possibly max)
    # 0x000, then 0x0050 - medium brightness
    # 0x000 then 0x0040 - fairly dim
    # 0x000 then 0x0030 - dim - suitable for text
    
    
    
    # 0x000F - very very dim.
    # - 0xFF seems to step brightness up.... 
    # - 0xFF seems to step brightness down.... 
    #0xFFFF, 0x0000 - off
    
    live=False
    
    while True:  # Main loop -- change to True
        
        # gura's channel
        #channel = 'UCoSrY_IQQVpmIRZ9Xf-y93g'
        
        # calli's channel
        channel = 'UCL_qhgtOy0dy1Agp8vkySQg'
        
        # reine
        #channel = 'UChgTyjG-pdNvxxhdsXfHQ5Q'
        
        # Each API query counts as 100 quota points, and the daily limit is 10k,
        # so you only get 100 polls per day = once every 14 minutes.
        # so we can't poll the API to know when streams start without sometimes missing the beginning.
        
        # a hacky alternative that works for now is to query the channel homepage,
        # and search for some random image tag that gets slapped on any livestream thumbnails
        # curl 'https://www.youtube.com/channel/UCL_qhgtOy0dy1Agp8vkySQg' | grep -o "hqdefault_live"
        # grep -o says only return match. If nothing, it wasn't found (not live).
        
        url = 'https://www.youtube.com/channel/' + channel
        resp = subprocess.check_output(['curl', url]).decode('utf-8')
        found = resp.find('hqdefault_live')
        
        if found > 0:
            print("Channel is live")
            
            if live==False:
                # start of stream
                #pixoo.draw_pic("/home/marc/Desktop/callismile2.png")
                #pixoo.draw_pic("/home/marc/Desktop/callism32.png")   # does this render better? Nope.
                # (latter was downsized by screenshotting thumbnail)
                #pixoo.draw_pic("/tmp/callism16.png")
                live=True
                
                # query API for stream details
                
                # poll API by calling curl system command (this works)
                #response=subprocess.check_output(['curl', 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCoSrY_IQQVpmIRZ9Xf-y93g&eventType=live&type=video&key=AIzaSyAqOvOpkps1J37ft_mrgJLIUKeUoNgOcEA']).decode('utf-8')
                
                # poll API by requests module (this also works, and seems more streamlined)
                rrr = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='
                        +channel+'&eventType=live&type=video&key=AIzaSyAqOvOpkps1J37ft_mrgJLIUKeUoNgOcEA')
                response = rrr.text
                
                # protect against errors
                if response.find("items") > 0:
                    jjj = json.loads(response)
                    streams = jjj["items"]
                    streamtitle = jjj["items"][0]["snippet"]["title"]
                    print("Calli is streaming: "+streamtitle)
                else:
                    print("error response getting stream data")
                
            else:
                # stream is still live. check again in 1min
                sleep(60.0)
            
        else:
            print("Channel not live")
            if live==True:
                # end of stream
                print("Stream ended!")
                pixoo.draw_pic("/home/marc/Desktop/calliblk.png")
                live=False
            # check again in 60s
            sleep(60.0)
            continue
        
