import socket
from math import log10, ceil
from time import sleep
from PIL import Image

#VIEWTYPES = {
#    "clock": 0x00,
#    "temp": 0x01,
#    "off": 0x02,
#    "anim": 0x03,
#    "graph": 0x04,
#    "image": 0x05,
#    "stopwatch": 0x06,
#    "scoreboard": 0x07
#}

#def view(ctx, type):
#    if (type in VIEWTYPES):
#        ctx.obj['dev'].send(switch_view(type))

#def clock(ctx, color, ampm):
#    if (color):
#        c = color_convert(Color(color).get_rgb())
#        ctx.obj['dev'].send(set_time_color(c[0], c[1], c[2], 0xff, not ampm))
#    else:
#        ctx.obj['dev'].send(switch_view("clock"))

#def temp(ctx, color, f):
#    if (color):
#        c = color_convert(Color(color).get_rgb())
#        ctx.obj['dev'].send(set_temp_color(c[0], c[1], c[2], 0xff, f))
#    else:
#        ctx.obj['dev'].send(switch_view("temp"))

#def switch_view(type):
#    h = [0x04, 0x00, 0x45, VIEWTYPES[type]]
#    ck1, ck2 = checksum(sum(h))
#    return [0x01] + mask(h) + mask([ck1, ck2]) + [0x02]

class Pixoo:
    CMD_SET_SYSTEM_BRIGHTNESS = 0x74
    CMD_SPP_SET_USER_GIF = 0xB1
    CMD_DRAWING_ENCODE_PIC = 0x5B

    BOX_MODE_CLOCK = 0
    BOX_MODE_TEMP = 1
    BOX_MODE_COLOR = 2
    BOX_MODE_SPECIAL = 3

    instance = None

    def __init__(self, mac_address):
        """
        Constructor
        """
        self.mac_address = mac_address
        self.btsock = None

    @staticmethod
    def get():
        if Pixoo.instance is None:
            Pixoo.instance = Pixoo(Pixoo.BDADDR)
            Pixoo.instance.connect()
        return Pixoo.instance

    def connect(self):
        """
        Connect to SPP.
        """
        print("Connecting to "+self.mac_address+"...")
        self.btsock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.btsock.connect((self.mac_address, 1))
        sleep(1)  # mandatory to wait at least 1 second
        print("Connected.")

    def disconnect(self, shutdown=0, close=1):
        # note 'shutdown' sends the disconnect signal to the resource,
        # whereas close deletes our handle to it. The latter *must* be called,
        # but the former will be called automatically if and only if we're the only
        # application with a handle to that resource open.
        # in order to not kill music, maybe only call close.
        if shutdown==1: self.btsock.shutdown(socket.SHUT_RDWR)   # force disconnection of the device
        if close==1: self.btsock.close()                # close our handle to the device

    def __spp_frame_checksum(self, args):
        """
        Compute frame checksum
        """
        return sum(args[1:]) & 0xFFFF

    def __spp_frame_encode(self, cmd, args):
        """
        Encode frame for given command and arguments (list).
        """
        payload_size = len(args) + 3

        # create our header
        frame_header = [1, payload_size & 0xFF, (payload_size >> 8) & 0xFF, cmd]

        # concatenate our args (byte array)
        frame_buffer = frame_header + args

        # compute checksum (first byte excluded)
        cs = self.__spp_frame_checksum(frame_buffer)

        # create our suffix (including checksum)
        frame_suffix = [cs & 0xFF, (cs >> 8) & 0xFF, 2]

        # return output buffer
        return frame_buffer + frame_suffix
        
#        01/05/00/5f/07/04/6f/00/02
#        --|len  |data    |chks |--
#        so data[5] is 5f/07/04
#        
#        01/03/00/27/02/2d/00/02
#        --|len  |data |chks |--
#        data[2] is 27/02
#        
#        we know that set box mode is 45....
#        
#        
#        01/03/00/42/45/00/02
#        --|len  |da|chk  |--
#        
#        
#        01/0d/00/45/00/01/00/01/00/00/00/ff/ff/ff/51/03/02
#        --|len  |45|-------------                |chk  |--

    def send(self, cmd, args):
        """
        Send data to SPP.
        """
        spp_frame = self.__spp_frame_encode(cmd, args)
        if self.btsock is not None:
            nb_sent = self.btsock.send(bytes(spp_frame))

    def set_system_brightness(self, brightness):
        """
        Set system brightness.
        """
        self.send(Pixoo.CMD_SET_SYSTEM_BRIGHTNESS, [brightness & 0xFF])

    def set_box_mode(self, boxmode, visual=0, mode=0):
        """
        Set box mode.
        """
        # original: works but also enables cycling of weather and temp too.
        #self.send(0x45, [boxmode & 0xFF, visual & 0xFF, mode & 0xFF])
        #self.send(0x45, [0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF])  # just white clock
        self.send(0x45, [boxmode & 0xFF, 0x01, visual & 0xFF, mode & 0xFF, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF])
        #               [ boxmode | ? | clockstyle | vis |  ? | ? | ? | R | G | B ]
        # vis: 0= clock, 1=clock, 2=weather only, 3 = weather/clock alternating
        # 4= temp, 5= temp/clock alt., 6=weather/temp alt., 7=clock/weather/temp alternating,
        # 8= planner, 9=planner/clock, 10=HOT, 11=clock/HOT, 12=HOT/weather/temp
        # 13=weather/HOT/clock, ..... 
        # seems like the above commands enable, but do not disable, the respective parts.

    def set_color(self, r, g, b):
        """
        Set color.
        """
        self.send(0x6F, [r & 0xFF, g & 0xFF, b & 0xFF])

    def encode_image(self, filepath):
        img = Image.open(filepath)
        return self.encode_raw_image(img)

    def encode_raw_image(self, img):
        """
        Encode a 16x16 image.
        """
        # ensure image is 16x16
        w, h = img.size
        if w == h:
            # resize if image is too big
            if w > 16:
                img = img.resize((16, 16))

            # so here it doesnt transmit an [rgba] value for every pixel,
            # but rather scans all pixels for an array of all unique [rgba]
            # combinations, defines that as the 'palette', and then sends pixels
            # as an array of palette indexes.
            # except it's not rgba, it's just rgb.
            # the "transparency" just comes from the fact that all completely transparent
            # pixels tend to be encoded with the same value, and for pomu pngs,
            # that value is (0,0,0,0) i.e. transparent *black* -> i.e. becomes black.
            # for calli (gimp) pngs, the transparent pixel was (255,255,255,0) -> i.e. white.
            # 
            # we can work around this by fixing any pixels with alpha = 0 (fully transparent)
            # to have rgb=0.
            

            # create palette and pixel array
            pixels = []
            palette = []
            first = True
            for y in range(16):
                for x in range(16):
                    pix = img.getpixel((x, y))

                    if len(pix) == 4:
                        r, g, b, a = pix
                        #if first == True:
                        #    print("first pixel: ",r,g,b,a)
                        #    first = False
                        if a == 0:
                            r, g, b, a = [0,0,0,0]
                    elif len(pix) == 3:
                        r, g, b = pix
                    if (r, g, b) not in palette:
                        palette.append((r, g, b))
                        idx = len(palette) - 1
                    else:
                        idx = palette.index((r, g, b))
                    pixels.append(idx)

            # encode pixels
            bitwidth = ceil(log10(len(palette)) / log10(2))
            nbytes = ceil((256 * bitwidth) / 8.0)
            encoded_pixels = [0] * nbytes

            encoded_pixels = []
            encoded_byte = ""
            for i in pixels:
                encoded_byte = bin(i)[2:].rjust(bitwidth, "0") + encoded_byte
                if len(encoded_byte) >= 8:
                    encoded_pixels.append(encoded_byte[-8:])
                    encoded_byte = encoded_byte[:-8]
            encoded_data = [int(c, 2) for c in encoded_pixels]
            #print("pixel one is ",pixels[0])
            #print("encoded is ",encoded_pixels[0])
            encoded_palette = []
            first = False
            for r, g, b in palette:
                if first == False: encoded_palette += [r, g, b]
                else:
                    encoded_palette += [0, 0, 0]
                    first = False
            #print("encoded palette is ",encoded_palette)
            return (len(palette), encoded_palette, encoded_data)
        else:
            print("[!] Image must be square.")

    def draw_gif(self, filepath, speed=100):
        """
        Parse Gif file and draw as animation.
        """
        # encode frames
        frames = []
        timecode = 0
        anim_gif = Image.open(filepath)
        for n in range(anim_gif.n_frames):
            anim_gif.seek(n)
            nb_colors, palette, pixel_data = self.encode_raw_image(anim_gif.convert(mode="RGBA"))
            frame_size = 7 + len(pixel_data) + len(palette)
            frame_header = [
                0xAA,
                frame_size & 0xFF,
                (frame_size >> 8) & 0xFF,
                timecode & 0xFF,
                (timecode >> 8) & 0xFF,
                0,
                nb_colors,
            ]
            frame = frame_header + palette + pixel_data
            frames += frame
            timecode += speed

        # send animation
        nchunks = ceil(len(frames) / 200.0)
        total_size = len(frames)
        for i in range(nchunks):
            chunk = [total_size & 0xFF, (total_size >> 8) & 0xFF, i]
            self.send(0x49, chunk + frames[i * 200 : (i + 1) * 200])

    def draw_anim(self, filepaths, speed=100):
        timecode = 0

        # encode frames
        frames = []
        n = 0
        for filepath in filepaths:
            nb_colors, palette, pixel_data = self.encode_image(filepath)
            frame_size = 7 + len(pixel_data) + len(palette)
            frame_header = [
                0xAA,
                frame_size & 0xFF,
                (frame_size >> 8) & 0xFF,
                timecode & 0xFF,
                (timecode >> 8) & 0xFF,
                0,
                nb_colors,
            ]
            frame = frame_header + palette + pixel_data
            frames += frame
            timecode += speed
            n += 1

        # send animation
        nchunks = ceil(len(frames) / 200.0)
        total_size = len(frames)
        for i in range(nchunks):
            chunk = [total_size & 0xFF, (total_size >> 8) & 0xFF, i]
            self.send(0x49, chunk + frames[i * 200 : (i + 1) * 200])

    def draw_pic(self, filepath):
        """
        Draw encoded picture.
        """
        nb_colors, palette, pixel_data = self.encode_image(filepath)
        frame_size = 7 + len(pixel_data) + len(palette)
        frame_header = [0xAA, frame_size & 0xFF, (frame_size >> 8) & 0xFF, 0, 0, 0, nb_colors]
        frame = frame_header + palette + pixel_data
        prefix = [0x0, 0x0A, 0x0A, 0x04]
        self.send(0x44, prefix + frame)


class PixooMax(Pixoo):
    """
    PixooMax class, derives from Pixoo but does not support animation yet.
    """

    def __init__(self, mac_address):
        super().__init__(mac_address)

    def draw_pic(self, filepath):
        """
        Draw encoded picture.
        """
        nb_colors, palette, pixel_data = self.encode_image(filepath)
        frame_size = 8 + len(pixel_data) + len(palette)
        frame_header = [
            0xAA,
            frame_size & 0xFF,
            (frame_size >> 8) & 0xFF,
            0,
            0,
            3,
            nb_colors & 0xFF,
            (nb_colors >> 8) & 0xFF,
        ]
        frame = frame_header + palette + pixel_data
        prefix = [0x0, 0x0A, 0x0A, 0x04]
        self.send(0x44, prefix + frame)

    def draw_gif(self, filepath, speed=100):
        raise "NotYetImplemented"

    def draw_anim(self, filepaths, speed=100):
        raise "NotYetImplemented"

    def encode_image(self, filepath):
        img = Image.open(filepath)
        img = img.convert(mode="P", palette=Image.ADAPTIVE, colors=256).convert(mode="RGBA")
        return self.encode_raw_image(img)

    def encode_raw_image(self, img):
        """
        Encode a 32x32 image.
        """
        # ensure image is 32x32
        w, h = img.size
        if w == h:
            # resize if image is too big
            if w > 32:
                img = img.resize((32, 32))

            # create palette and pixel array
            pixels = []
            palette = []
            for y in range(32):
                for x in range(32):
                    pix = img.getpixel((x, y))

                    if len(pix) == 4:
                        r, g, b, a = pix
                        if a == 0:
                            r, g, b = (0, 0, 0)
                    elif len(pix) == 3:
                        r, g, b = pix
                    if (r, g, b) not in palette:
                        palette.append((r, g, b))
                        idx = len(palette) - 1
                    else:
                        idx = palette.index((r, g, b))
                    pixels.append(idx)

            # encode pixels
            bitwidth = ceil(log10(len(palette)) / log10(2))
            nbytes = ceil((256 * bitwidth) / 8.0)
            encoded_pixels = [0] * nbytes

            encoded_pixels = []
            encoded_byte = ""

            # Create our pixels bitstream
            for i in pixels:
                encoded_byte = bin(i)[2:].rjust(bitwidth, "0") + encoded_byte

            # Encode pixel data
            while len(encoded_byte) >= 8:
                encoded_pixels.append(encoded_byte[-8:])
                encoded_byte = encoded_byte[:-8]

            # If some bits left, pack and encode
            padding = 8 - len(encoded_byte)
            encoded_pixels.append(encoded_byte.rjust(bitwidth, "0"))

            # Convert into array of 8-bit values
            encoded_data = [int(c, 2) for c in encoded_pixels]
            encoded_palette = []
            for r, g, b in palette:
                encoded_palette += [r, g, b]
            return (len(palette), encoded_palette, encoded_data)
        else:
            print("[!] Image must be square.")
