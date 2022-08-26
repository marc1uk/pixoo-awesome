from os import getenv
from time import sleep
from PIL import Image
# for youtube
#import subprocess
import json
import requests

import modules.pixoo_client as pixc

#load_dotenv("local.env", verbose=True)

if __name__ == "__main__":
    # tivoo
    bt_mac_addr = '11:75:58:1E:A9:52'
    
#    print(bt_mac_addr)
    pixoo = pixc.Pixoo(bt_mac_addr)
    pixoo.connect()
    
#    print("drawing pic")
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
#    pixoo.draw_pic("/home/marc/Desktop/cf3e227de5571d7e.png")
    
    print("show time")
    # args are: mode, ??, style.
    # style being e.g. what style of clock to show, for clock mode.
    # pixoo.BOX_MODE_CLOCK (00) shows the clock, but starts scrolling through everything.
    # (see pixoo_client.py, 'fixed')
    # pixoo.BOX_MODE_TEMP (01) colour cycle mode, but also seems to interact with the brightness...
    # this can be worked around by setting colour mode then setting brightness.
    # pixoo.BOX_MODE_COLOR (02) sets it to 'HOT' animation
    # pixoo.BOX_MODE_SPECIAL (03) sets it to colour - so far, just green.
    # 0x04 = equalizer
    # 0x05 = user channel - so far, only channel 1.
    # 0x06 = scoreboard. following bits set the scores, but this function doesn't do it properly.
    # 0x07 = reset scoreboard?
    pixoo.set_box_mode(0x00, 0x00, 0x00)
    # this works
    #pixoo.set_system_brightness(0xFF)
    
    #pixoo.draw_pic("/home/marc/LinuxSystemFiles/bitbash/test.bmp")
    #sleep(1.0)
    #pixoo.draw_pic("/home/marc/Desktop/callismile2.png")
    #print("shown")
    
    
#    live = False
#    while True:  # Main loop
#        
#        # this works - call curl system command
#        #response=subprocess.check_output(['curl', 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCoSrY_IQQVpmIRZ9Xf-y93g&eventType=live&type=video&key=AIzaSyAqOvOpkps1J37ft_mrgJLIUKeUoNgOcEA']).decode('utf-8')
#        
#        # this also works, more streamlined
#        #rrr = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCoSrY_IQQVpmIRZ9Xf-y93g&eventType=live&type=video&key=AIzaSyAqOvOpkps1J37ft_mrgJLIUKeUoNgOcEA')
#        rrr = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCoSrY_IQQVpmIRZ9Xf-y93g&eventType=live&type=video&key=AIzaSyAqOvOpkps1J37ft_mrgJLIUKeUoNgOcEA')
#        
#        response = rrr.text
#        jjj = json.loads(response)
#        streams = jjj["items"]
#        
#        if len(streams) > 0 and live==False:
#            # start of stream
#            streamtitle = jjj["items"][0]["snippet"]["title"]
#            print("Calli is streaming: "+streamtitle)
#            pixoo.draw_pic("/home/marc/Desktop/callismile2.png")
#            live=True
#        elif len(streams) == 0 and live==True:
#            # end of stream
#            print("Stream ended!")
#            pixoo.draw_pic("/home/marc/Desktop/calliblk.png")
#            live=False
#        
#        sleep(10.0)
