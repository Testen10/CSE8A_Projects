from PIL import Image

def changeLineColor(color, image):
    """docstring
        changing line color of the image
        
        input: image

        If the image's maximum rgb value (either r,g,b) is smaller than the threshold, apply subtraction on the pixel by the value of color

        threshold set as 255*0.5
    """
    threshold = 255*0.5
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if max(list(image.getpixel((x,y)))) < threshold: 
                rgb = image.getpixel((x,y))
                image.putpixel((x,y), 
                               (max(rgb[0]-color[0], 0),
                               max(rgb[1]-color[1], 0),
                               max(rgb[2]-color[2], 0)))

    return image

def addition(color, image):
    """docstring
        applying addition filter on the image

        input: image, color(rgb value in tuple)

        adding color's rgb value to the image's rgb value
    """
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = image.getpixel((x,y))
            mod_rgb = (min(255,rgb[0]+color[0]),
                       min(255,rgb[1]+color[1]), 
                       min(255,rgb[2]+color[2]))

            image.putpixel((x,y),mod_rgb)

    return image

def add_background(image, background):
    """docstring
        compositing background on image

        input: image, background
        
        if the pixel of the image is white, change it to pixel of the background
    """
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = image.getpixel((x,y))
            if rgb == (255,255,255): # color key // erase white background from original image & add the image to the background
                bg_pixel = background.getpixel((x,y))
                image.putpixel((x,y), bg_pixel)

    return image

def add_frame(image,frame):
    """docstring
        compositing frame on image

        input: image, frame
        
        if the pixel of the frame is in the green range, change the pixel of image to the pixel of frame
    """
    green_range = (10,250,10) # 
    for x in range(frame.size[0]):
            for y in range(frame.size[1]):
                frame_rgb = frame.getpixel((x,y))
                if not (frame_rgb[0]<green_range[0] and frame_rgb[1]>green_range[1] and frame_rgb[2]<green_range[2]): # chroma key // put frame on the image
                    image.putpixel((x,y), frame_rgb)

    return image

def add_watermark(image,watermark): 
    """docstring
        overlay the watermark on the image

        input: image, watermark
        
        only apply the filter on the white pixel of watermark(erase black background)
        if the image's average rgb value is bigger than threshold value, screen the watermark on the image
        otherwise, multiply the watermark on the image
    """
    threshold = 255*0.5
    for x in range(image.size[0]):
            for y in range(image.size[1]):
                rgb = image.getpixel((x,y))
                wm_rgb = watermark.getpixel((x,y))
                if wm_rgb==(255,255,255):
                    if sum(rgb)/3<threshold:
                        mod_rgb = (wm_rgb[0]*2*rgb[0]//255,
                                   wm_rgb[1]*2*rgb[1]//255,
                                   wm_rgb[2]*2*rgb[2]//255)
                    else:
                        mod_rgb = ((255 - 2*(255-wm_rgb[0])*(255-rgb[0])//255),
                                   (255 - 2*(255-wm_rgb[1])*(255-rgb[1])//255),
                                   (255 - 2*(255-wm_rgb[2])*(255-rgb[2])//255))


                    image.putpixel((x,y), mod_rgb)

    return image

def concat_img(img_list):
    """docstring
        concat six images

        input: six images to concat
        
        make an empty image of size 2*width, 3*height & change the empty image's pixel value into the image's pixel value
    """
    width, height = img_list[0].size
    return_img = Image.new(mode="RGB", size=(width*2, height*3))

    range_list = [(width,height),(width*2,height),(width,height*2),(width*2,height*2),(width,height*3),(width*2,height*3)]
    
    
    for x in range(return_img.size[0]):
        for y in range(return_img.size[1]):
            if x<range_list[0][0] and y<range_list[0][1]: rgb = img_list[0].getpixel((x,y))
            elif x<range_list[1][0] and y<range_list[1][1]: rgb = img_list[1].getpixel((x-width,y))
            elif x<range_list[2][0] and y<range_list[2][1]: rgb = img_list[2].getpixel((x,y-height))
            elif x<range_list[3][0] and y<range_list[3][1]: rgb = img_list[3].getpixel((x-width,y-height))
            elif x<range_list[4][0] and y<range_list[4][1]: rgb = img_list[4].getpixel((x,y-height*2))
            else: rgb = img_list[5].getpixel((x-width,y-height*2))
            
 
            return_img.putpixel((x,y), rgb)

    return return_img
            
img = Image.open('image/original.jpeg')
img = img.resize((img.size[0]//2,img.size[1]//2))
bg = Image.open('image/background.jpeg')
bg = bg.resize((bg.size[0]//2,bg.size[1]//2))
fm = Image.open('image/frame.jpeg')
fm = fm.resize((fm.size[0]//2,fm.size[1]//2))
wm = Image.open('image/watermark.jpeg')
wm = wm.resize((wm.size[0]//2,wm.size[1]//2))

lineedit_img = changeLineColor((50,50,0), img.copy())
add_img = addition((16,14,40), lineedit_img.copy())
bgadd_img = add_background(add_img.copy(), bg.copy())
fmadd_img = add_frame(bgadd_img.copy(), fm.copy())
wmadd_img = add_watermark(fmadd_img.copy(), wm.copy())

result = concat_img([img, lineedit_img, add_img, bgadd_img, fmadd_img, wmadd_img])

result.show()
result.save("result.png")