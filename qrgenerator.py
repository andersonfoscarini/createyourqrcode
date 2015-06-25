__author__ = 'anderson'

from qrcode import *
from PIL import Image, ImageOps


def create_qrcode(text, image_path, newversion):
    qr = QRCode(
        version=4,
        error_correction=ERROR_CORRECT_L,
        box_size=9,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    im = qr.make_image()
    #im.save("code.png")
    #print image_path
    imagef=Image.open(image_path)
    imagef=imagef.convert('L')
    if im.size < imagef.size:
        imagef.thumbnail(im.size)
        newsize0 = (im.size[0] - imagef.size[0])
        newsize1 = (im.size[1] - imagef.size[1])
        newsize = (newsize0+18, newsize1+18)
        thum = ImageOps.expand(imagef,border=newsize, fill='white')
        thum = ImageOps.fit(thum,im.size)
    else:
        thum = ImageOps.fit(imagef,im.size)

    #thum.save('thum.png')
    if newversion is not None:
        thum1 = thum.filter(ImageFilter.FIND_EDGES)

        thum1 = thum1.filter(ImageFilter.EDGE_ENHANCE_MORE)
        thum1 = thum1.filter(ImageFilter.EDGE_ENHANCE_MORE)
        thum2 = thum1.filter(ImageFilter.GaussianBlur)
        thum2 = thum2.filter(ImageFilter.GaussianBlur)

        thum2 = ImageOps.autocontrast(thum2)
        thum2 = ImageOps.equalize(thum2)
        thum2 = thum2.filter(ImageFilter.SHARPEN)
        thum2 = thum2.filter(ImageFilter.SHARPEN)
        for i in range(0,im.size[0]):
            for j in range(0, im.size[1]):
                thum2.putpixel((i,j), thum2.getpixel((i,j))+70)
    for i in range(0, im.size[0]-1):
        for j in range(0, im.size[1]-1):
            cc = thum.getpixel((i,j)) #// current color
            if cc < 128:
                rc=0
            else:
                rc=255      #real (rounded) color
            err = cc-rc              # error amount
            thum.putpixel((i,j), rc)#   saving real color
            if j+1 < im.size[1]:
                thum.putpixel((i,j+1), thum.getpixel((i,j+1))+(err*7)/16)# if right neighbour exists
            if i+1 == im.size[0] :
                pass   #// if we are in the last line
            if j > 0 :
                thum.putpixel((i+1,j-1), thum.getpixel((i+1,j-1))+(err*3)/16) #bottom left neighbour
                thum.putpixel((i+1,j), thum.getpixel((i+1,j))+(err*5)/16)  #bottom neighbour
            if j+1 < im.size[1] :
                thum.putpixel((i+1,j+1), thum.getpixel((i+1,j+1))+(err*1)/16) #bottom right neighbour

    for i in range(0,81):
        for j in range(0,81):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(im.size[0]-81,thum.size[0]):
        for j in range(0,81):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(0,81):
        for j in range(im.size[1]-81, im.size[1]):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(234,279):
        for j in range(234, 279):
            thum.putpixel((i,j), im.getpixel((i,j)))

    for i in range(81-9,81):
        for j in range(0,im.size[1]):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(0,im.size[0]):
        for j in range(81-9,81):
            thum.putpixel((i,j), im.getpixel((i,j)))


    for i in range(0,im.size[0]):
        for j in range(0, 18):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(0,im.size[0]):
        for j in range(im.size[1]-18, im.size[1]):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(0,18):
        for j in range(0, im.size[1]):
            thum.putpixel((i,j), im.getpixel((i,j)))
    for i in range(im.size[0]-18,im.size[0]):
        for j in range(0, im.size[1]):
            thum.putpixel((i,j), im.getpixel((i,j)))

    x=21
    while x < im.size[0]:
        y=21
        while y < im.size[1]:
            if x < 81 and y < 81 or x>im.size[0]-81 and y < 81 or x<81 and y>im.size[1]-81 or x>233 and x<=279 and y>233 and y <=279:
                pass
            else:
                if newversion is not None:
                    for l in range(-3,6):#submodulos todos
                        for m in range(-3,6):
                            original = thum.getpixel((x+l, y+m))
                            from_qrcode = im.getpixel((x+l, y+m))
                            threshold = float(thum2.getpixel((x+l,y+m)))/255.0
                            newvalue = original*threshold + (1-threshold)*from_qrcode
                            thum.putpixel((x+l, y+m), newvalue)
                for l in range(0,3):#submodulo central
                    for m in range(0,3):
                        thum.putpixel((x+l,y+m), im.getpixel((x+l, y+m)))
            y+=9
        x+=9

    if newversion is not None:
        for i in range(0,im.size[0]):
            for j in range(0, im.size[1]):
                if thum.getpixel((i,j)) < 180:
                    thum.putpixel((i,j), 0)
    #thum.save(image_path+'qr.jpg')
    return thum
   # thum.save(text.sub('http://www','').gsub('.','_')+'.png')


