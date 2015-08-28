
from optparse import OptionParser
from PIL import Image, ImageDraw
import sys

def is_while (pix):
    if pix[0] == 0 and pix[1] == 0 and pix[2] == 0:
        return True
    return False

if __name__ == "__main__":
    print ("Alaphadots!")
    parser = OptionParser ()
    parser.add_option ('-f', '--file', dest='filename',
                       help='Input file. The image to generate from',
                       metavar='FILE')
    parser.add_option ('-s', '--size', dest='charsize',
                       help='AxB where A is width, B is height, in pixels',
                       metavar='AxB')
    parser.add_option ('-o', '--offset', dest='offset', metavar='offset',
                       default=1, type='int',
                       help='How many pixels in between chars')
    parser.add_option ('-i', '--invert', dest='invert', default=True,
                       action='store_false',
                       help='Invert the resulting bytes')
    parser.add_option ('-d', '--dump', dest='dumpfile', metavar='FILE',
                       help='File to dump the data in')
    parser.add_option ('-t', '--format', dest='format', metavar='FORMAT_STRING',
                       help='printf style format string, %s will be replaced '
                       'with the data',
                       default='const uint8_t data[] PROGMEM = { %s }')
        
    (options, args) = parser.parse_args ()

    if options.filename == None:
        print ("Error: No file selected. Select with -f / --file")
        sys.exit (-1)
    if options.charsize == None:
        print ("No charsize selected, assuming 5x8")
        options.charsize = "5x8"

    char = {}
    try:
        splt = options.charsize.split ("x")
        char['width'] = int (splt[0])
        char['height'] = int (splt[1])
        print (char)
    except (ValueError, IndexError):
        print ("Error: Charsize must be AxB, look up the help")
        exit (-1)
        
    try:
        im = Image.open (options.filename)
        outim = Image.new ("RGB", im.size, "white")
        outdraw = ImageDraw.Draw (outim)
        pixels = im.load ()
        print ("Image loaded. Size: %s" % str(im.size))
        stringbuff = ""
        # TODO: add more types of encoding
        col_ad = 0
        row_ad = 0
        chars_done = 0
        cols_done = 0
        bytes_done = 0
        while col_ad < im.size[0]:
            res = 0
            row_ad = 0
            while row_ad < char['height']:
                pix = pixels[col_ad, row_ad]
                #print (pix)
                if not is_while (pix):
                    res |= 1 << (row_ad % 8)
                    outdraw.point ((col_ad, row_ad), fill=(0,0,0))
                    #outim.putpixel (, (255,255,255))
                if row_ad % 8 == 7:
                    if options.invert:
                        res = ~res
                        res &= 0xFF
                    stringbuff += ("0x%02x, " % res)
                    bytes_done += 1
                    res = 0
                row_ad += 1
            stringbuff += '\n'
            col_ad += 1
            cols_done += 1
            if cols_done == char['width']:
                col_ad += options.offset
                chars_done += 1
                cols_done = 0
            #if chars_done == 2:
            #    break
        if options.dumpfile == None:
            print (stringbuff, end='')
        else:
            with open (options.dumpfile, 'w') as f:
                f.write (options.format % stringbuff)
        print ("Done %d chars. (%d bytes)" % (chars_done, bytes_done))
        del outdraw
        outim.save ("rendered.png")
                
    except ValueError:
        print ("Bleh!")
        
    print (options, args)
