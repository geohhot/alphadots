
from optparse import OptionParser
from PIL import Image
import sys

def is_while (pix):
    if pix[0] == 0 and pix[1] == 0 and pix[2] == 0:
        return True
    return False

if __name__ == "__main__":
    print ("Alaphadots!")
    parser = OptionParser ()
    parser.add_option ('-f', '--file', dest="filename",
                       help="The image to generate from",
                       metavar="FILE")
    parser.add_option ('-s', '--size', dest='charsize',
                       help="AxB where A is width, B is height, in pixels",
                       metavar="AxB")
    parser.add_option ('-p', '--offset', dest='offset', metavar='offset',
                       default=1, type="int",
                       help="How many pixels in between chars")
    parser.add_option ('-i', '--invert', dest='invert', default=True,
                       action="store_false",
                       help="Invert the resulting bytes")
        
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
        pixels = im.load ()
        print ("Image loaded. Size: %s" % str(im.size))

        # TODO: add more types of encoding
        col_ad = 0
        row_ad = 0
        chars_done = 0
        cols_done = 0
        while col_ad < im.size[0]:
            res = 0
            row_ad = 0
            while row_ad < char['height']:
                pix = pixels[col_ad, row_ad]
                #print (pix)
                if not is_while (pix):
                    res |= 1 << row_ad
                row_ad += 1
            if options.invert:
                res = ~res
                res &= 0xFF
            print ("0x%02x," % res)
            col_ad += 1
            cols_done += 1
            if cols_done == char['width']:
                col_ad += options.offset
                chars_done += 1
                cols_done = 0
#            if chars_done == 2:
#               break
            if col_ad == im.size[0]:
                break
                
    except ValueError:
        print ("Bleh!")
        
    print (options, args)
