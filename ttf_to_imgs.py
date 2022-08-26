# pip install Pillow
from PIL import Image, ImageFont, ImageDraw
# converts a ttf font to a set of images of each character.
# filenames are the ASCII code of the corresponding character

# use a truetype font (.ttf)
# font file from fonts.google.com (https://fonts.google.com/specimen/Courier+Prime?query=courier)
font_path = "/home/marc/LinuxSystemFiles/pixoo-awesome/silkscreen/"
font_name = "slkscr.ttf"
out_path = font_path

font_size = 8 # px
font_color = "#000000" # HEX Black

# Create Font using PIL
font = ImageFont.truetype(font_path+font_name, font_size)

# Copy Desired Characters from Google Fonts Page and Paste into variable
desired_characters = 'abcdefghijklmnopqrstuvwxyz.0123456789"\'?!@#&<>:-,()*'
#desired_characters = "ABCČĆDĐEFGHIJKLMNOPQRSŠTUVWXYZŽabcčćdđefghijklmnopqrsštuvwxyzž1234567890‘?’“!”(%)[#]{@}/&\<-+÷×=>®©$€£¥¢:;,.*"

# Loop through the characters needed and save to desired location
for character in desired_characters:
    
    # Get text size of character
    width, height = font.getsize(character)
    
    # Create PNG Image with that size
    img = Image.new("RGBA", (width-1, height+1))
    draw = ImageDraw.Draw(img)
    
    # Draw the character
    draw.text((0, 0), str(character), font=font, fill=font_color)  # (-2,0)
    
    # Save the character as png
    try:
        img.save(out_path + str(ord(character)) + ".png")
    except:

        print("[-] Couldn't Save:\t"+character)
