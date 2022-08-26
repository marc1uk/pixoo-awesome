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
    # tivoo
    bt_mac_addr = '11:75:58:1E:A9:52'
    
#    print(bt_mac_addr)
    pixoo = pixc.Pixoo(bt_mac_addr)
    #pixoo.connect()
    
    # start out on clock mode.
    pixoo.set_box_mode(0x00, 0x00, 0x00)
    
    # switch to emote when live
    live=False
    
    while True:  # Main loop
        
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
                pixoo.connect()
                pixoo.draw_pic("/home/marc/Desktop/callismile2.png")
                #pixoo.draw_pic("/home/marc/Desktop/callism32.png")   # does this render better? Nope.
                # (latter was downsized by screenshotting thumbnail)
                #pixoo.draw_pic("/tmp/callism16.png")
                # close the socket so we stop the hiss.....
                # this doesn't stop the hiss - the audio sink link remains open...
                # but at least we can disconnect it from bluez, and it'll recover.
                pixoo.disconnect()  # close our handle to the socket
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
                # back to clock mode
                pixoo.connect()
                pixoo.set_box_mode(0x00, 0x00, 0x00)
                # close the socket so we stop the hiss
                pixoo.disconnect()  # close our handle to the socket
                live=False
            # check again in 60s
            sleep(60.0)
            continue
        
