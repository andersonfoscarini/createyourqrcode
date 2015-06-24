__author__ = 'anderson'

from qrcode import *
from PIL import Image, ImageOps


def create_qrcode(text, image_path):
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
    imagef.thumbnail(im.size)
    newsize0 = (im.size[0] - imagef.size[0])
    newsize1 = (im.size[1] - imagef.size[1])
    newsize = (newsize0+18, newsize1+18)
    thum = ImageOps.expand(imagef,border=newsize, fill='white')
    thum = ImageOps.fit(thum,im.size)

    #thum.save('thum.png')

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
                thum.putpixel((x,y), im.getpixel((x,y)))
                thum.putpixel((x+1,y), im.getpixel((x+1,y)))
                thum.putpixel((x+2,y), im.getpixel((x+2,y)))
                thum.putpixel((x,y+1), im.getpixel((x,y+1)))
                thum.putpixel((x,y+2), im.getpixel((x,y+2)))
                thum.putpixel((x+1,y+1), im.getpixel((x+1,y+1)))
                thum.putpixel((x+1,y+2), im.getpixel((x+1,y+2)))
                thum.putpixel((x+2,y+1), im.getpixel((x+2,y+1)))
                thum.putpixel((x+2,y+2), im.getpixel((x+2,y+2)))
            y+=9
        x+=9
    #thum.save(image_path+'qr.jpg')
    return thum
   # thum.save(text.sub('http://www','').gsub('.','_')+'.png')


