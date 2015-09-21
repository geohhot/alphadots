def set_font (font):
    k = gimp.image_list()[0]
    layers = k.layers
    for lay in layers:
        if lay.name == "Text":
            for l in lay.layers:
 	        nm = pdb.gimp_item_get_name (l)
 	        pdb.gimp_text_layer_set_font(l, font)

                
def set_size (size):
    k = gimp.image_list()[0]
    layers = k.layers
    for lay in layers:
        if lay.name == "Text":
            for l in lay.layers:
 	        nm = pdb.gimp_item_get_name (l)
                pdb.gimp_text_layer_set_font_size(l, size, 0)


#CA2536
def set_color (color):
    k = gimp.image_list()[0]
    layers = k.layers
    for lay in layers:
        if lay.name == "Text":
            for l in lay.layers:
 	        nm = pdb.gimp_item_get_name (l)
                pdb.gimp_text_layer_set_color(l, color)
    

def draw_offsets (width = 40, offset=10, color=(120,120,120)):
    # ( x + offset ) * k = width
    k = gimp.image_list()[0]
    layers = k.layers
    #print (dir (layers))
    bg = None
    for l in layers:
        if l.name == "Background":
            bg = l
    if bg == None:
        return
    x = width
    y = 0
    of = 0
    while x < bg.width:
        of = 0
        while of < offset:
            y = 0
            while y < bg.height:
                bg.set_pixel (x + of,y, color)
                y += 1
            of += 1
        x += width + offset
    bg.flush ()
    bg.visible = False
    bg.visible = True


def draw_text (alphabet="0123456789", color=(0,0,0),
               font="", fontsize=43, unit=0,
               offset=10, width=40):
    k = gimp.image_list ()[0]
    bg = None
    for l in k.layers:
        if l.name == "Background":
            bg = l
    layer_group = pdb.gimp_layer_group_new (k)
    k.add_layer (layer_group)
    layer_group.name = "Text"
    letter_num = 0
    for l in alphabet:
        tl = pdb.gimp_text_layer_new (k, l, font, fontsize, unit)
        #tl.parent = layer_group
        k.add_layer (tl)
        pdb.gimp_text_layer_set_color (tl, color)
        pdb.gimp_text_layer_resize (tl, width, bg.height)
        pdb.gimp_text_layer_set_justification (tl, 2)
        #pdb.gimp_text_layer_set_line_spacing (tl, 10)
        #pdb.gimp_text_layer_set_antialias(tl, True)
        pdb.gimp_text_layer_set_hinting(tl, False, False)
        pdb.gimp_layer_set_offsets (tl, (offset + width) * letter_num, 0)
        letter_num += 1

