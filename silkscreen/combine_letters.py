from os import getenv, stat, path
from time import sleep
from PIL import Image
import PIL.ImageOps  # set char colours as white not black!
import os, sys
#import numpy as np

curdir = os.path.dirname(os.path.realpath(__file__))

def add_letter(base, letter, topleft):
    ascii = ord(letter)
    filename = curdir + '/' + str(ascii)+".png"
    next_letter = Image.open(filename)
    # until we convert the chars to white, do it on the fly
    r, g, b, a = next_letter.split()
    r = g = b = r.point(lambda i: 255)
    next_letter = Image.merge('RGBA', (r, g, b, a))
    w, h = next_letter.size
    #print("add_letter: ",topleft)
    w = max(2,w)   # some punctuations have no padding
    if letter == ':':
        # for single-pixel wide punctuations, shift them right
        # for better centering? might be better for commas and fullstops though...
        w = 1
        topleft[0] += 1
    # combine with working canvas
    base.alpha_composite(next_letter,(topleft[0],topleft[1]))
    topleft[0] += (w+1)
    #print("add_letter: ",topleft)
    return h

def write_chars(base, string, topleft):
    h = 0
    chars = list(string)
    for achar in chars:
        h = add_letter(base, achar, topleft)
        #print("write_chars: ",topleft)
    return h

def write_line(base, string, topleft):
    h = write_chars(base, string, topleft)
    #print("write_line: ",topleft)
    topleft[0] = 2  # XXX slightly better centering
    topleft[1] += (h+2)

def draw_text(inputtext):
    topleft=[2,0]  # XXX slightly better centering
    base = Image.new("RGBA", (32, 32), (0, 0, 0, 0))  # Create a base new image
    textlines = inputtext.splitlines()
    for line in textlines:
        write_line(base, line, topleft)
    base.save("tmp1.png")
    # inverted version
    r, g, b, a = base.split()
    r = g = b = r.point(lambda i: 0)
    base = Image.merge('RGBA', (r, g, b, a))
    whitebg = Image.new("RGBA", (32, 32), (255, 255, 255, 255))
    whitebg.alpha_composite(base)
    whitebg.save("tmp2.png")
    
    

if __name__ == "__main__":
#    topleft=(0,0)
#    base = Image.new("RGBA", (32, 32), (0, 0, 0, 0))  # Create a base new image
#    next_letter = Image.open("49.png")    # 
#    base.alpha_composite(next_letter,topleft)                 # Add to the base image
#    base.save("tmp1.png")
#    
#    print("topleft is ",topleft)
#    print("size is ",next_letter.size)
##    topleft = tuple(np.add(topleft,next_letter.size))
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    print("topleft is ",topleft)
#    
#    next_letter = Image.open("54.png")    # 
#    base.alpha_composite(next_letter,topleft)                 # Add to the base image
#    base.save("tmp2.png")
#    
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("58.png")  # ':'
#    base.alpha_composite(next_letter,topleft)
#    
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("51.png")
#    base.alpha_composite(next_letter,topleft)
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("56.png")
#    base.alpha_composite(next_letter,topleft)
#    
#    # so far so good
#    # next line
#    topleft = (0, topleft[1]+h+2)
#    
#    next_letter = Image.open("48.png")
#    base.alpha_composite(next_letter,topleft)
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("54.png")
#    base.alpha_composite(next_letter,topleft)
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("58.png")
#    base.alpha_composite(next_letter,topleft)
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("51.png")
#    base.alpha_composite(next_letter,topleft)
#    w, h = next_letter.size
#    topleft = (topleft[0]+w+1, topleft[1])
#    next_letter = Image.open("50.png")
#    base.alpha_composite(next_letter,topleft)
#    base.save("tmp3.png")
    
    topleft=[2,0]  # XXX slightly better centering
    base = Image.new("RGBA", (32, 32), (0, 0, 0, 0))  # Create a base new image
    
    #write_line(base, "14:32", topleft)
    #write_line(base, "05:02", topleft)
    #write_line(base, "12345", topleft) # the max amount of text you can fit is about 3 lines of 5 chars
    
    inputtext = sys.argv[1]
    textlines = inputtext.splitlines()
    for line in textlines:
        write_line(base, line, topleft)
    base.save("tmp1.png")
    
    # also save inverted image - 1. split the text layer
    r, g, b, a = base.split()
    # 2. invert the text colour
    r = g = b = r.point(lambda i: 0)
    # 3. recombine into an image
    base = Image.merge('RGBA', (r, g, b, a))
    # 4. make a white bg
    whitebg = Image.new("RGBA", (32, 32), (255, 255, 255, 255))
    # 5. merge the black text onto the white bg
    whitebg.alpha_composite(base)
    whitebg.save("tmp2.png")
    
