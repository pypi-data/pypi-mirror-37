# -*- coding: UTF-8 -*-
"""
TCM 32.1 classes.

..  Copyright (C) MpicoSys-Embedded Pico Systems, all Rights Reserved.
    This source code and any compilation or derivative thereof is the
    proprietary information of MpicoSys and is confidential in nature.
    Under no circumstances is this software to be exposed to or placed
    under an Open Source License of any type without the expressed
    written permission of MpicoSys.
"""

__copyright__ = "Copyright (C) MpicoSys-Embedded Pico Systems"
__author__ = "Paweł Musiał <pawel.musial@mpicosys.com>"
__version__ = "2.0"

from .TCGen2 import TCGen2

from PIL import Image


# TODO convert to new format
class TCM312v320(TCGen2):
    """
    Class used to convert images TCM 
    """

    resolution_x = 1440
    resolution_y = 2560

    supported_number_of_colors = [2, 4]
    panel_type = '312'

    def __init__(self):
        #self.imagedata = None
        super().__init__()

    def get_epd_header(self,image):
        # EPD file format for 31.2
        return [0x3F,0x05,0xA0,0x0A,0x00,0x01,0x07]+[0x00,]*9


    def convert(self,img):
        if self.is_image_two_bit(img):
            return list(self.convert_2bit(img)) # seems Type7
        else:
            return list(self.convert_1bit(img)) # seems Type0

    def convert_1bit(self, img):

        img=img.convert('P')
        img=img.transpose(Image.FLIP_LEFT_RIGHT)
        imgbytes = list(img.tobytes())
        imgnewbytes = list(int(len(imgbytes)) * b'\x00')

        trans1=( # new, original
            (6,7),
            (4,6),
            (2,5),
            (0,4),
            (14,3),
            (12,2),
            (10,1),#
            (8,0),
            (7,15),
            (5,14),
            (3,13),
            (1,12),
            (15,11),
            (13,10),
            (11,9),##
            (9,8)
           )

        for i in range(int(len(imgbytes)/16)):
            for t, f in trans1:
                imgnewbytes[16 * (i) + t] = imgbytes[16 * (i) + f]
        imgnew = Image.frombytes('P', img.size, bytes(imgnewbytes))
        palette = []
        for i in range(256):
            p = 0xFF
            if i > 0:
                p = 0x00
            palette.extend((p, p, p))
        assert len(palette) == 768
        imgnew.putpalette(palette)
        newstr = imgnew.convert('1').tobytes()

        return list(newstr)

    def convert_2bit(self, img, dither=True):
        (img_width, img_height) = img.size
        assert img_width == 1440
        assert img_height == 640 * 4

        img = img.convert('P')
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

        pal = []
        for i in range(63):
            pal.extend([0, 0, 0])
        for i in range(64):
            pal.extend([85, 85, 85])
        for i in range(64):
            pal.extend([170, 170, 170])
        for i in range(65):
            pal.extend([255, 255, 255])
        assert len(pal) == 768

        if dither:
            img = img.convert('P', None, Image.FLOYDSTEINBERG, Image.WEB, 4)
            print
            "dithering!"
        img.save("img.png")
        img = img.convert('L')
        img.putpalette(pal)
        img = img.convert('L')

        imgbytes = list(img.tobytes())
        imgnewbytes = list(len(imgbytes) * b'\x00')

        trans1 = (  # new, original
            (6, 7),
            (4, 6),
            (2, 5),
            (0, 4),
            (14, 3),
            (12, 2),
            (10, 1),
            (8, 0),
            (7, 15),
            (5, 14),
            (3, 13),
            (1, 12),
            (15, 11),
            (13, 10),
            (11, 9),
            (9, 8)
        )

        for i in range(int(len(imgbytes) / 16)):
            for t, f in trans1:
                imgnewbytes[16 * (i) + t] = imgbytes[16 * (i) + f]

        imgnew = Image.frombytes('P', img.size, bytes(imgnewbytes))

        imgbytes = list(imgnew.tobytes())

        palette = {0: 3, 85: 2, 170: 1, 255: 0}  # dictionary
        i = 0
        for byte in imgbytes:
            imgbytes[i] = palette[byte]
            i += 1

        (imgnewbytes1, imgnewbytes0) = self.rawImg2binData(imgbytes)

        xBytes = int(imgnew.size[0] / 8)
        newstr = []
        for y in range(imgnew.size[1]):
            newstr.extend(imgnewbytes1[y * xBytes:(y + 1) * xBytes])
            newstr.extend(imgnewbytes0[y * xBytes:(y + 1) * xBytes])

        return bytes(list(newstr))

    def rawImg2binData(self, imgbytes):
        imgnewbytes0 = list(int(len(imgbytes) / 8) * b'\x00')
        imgnewbytes1 = list(int(len(imgbytes) / 8) * b'\x00')

        pointer = 0
        i = 0
        loop_len = len(imgbytes)
        while i < loop_len:
            temp = (((imgbytes[i + 0] & 1) << 7) & 0x80) | \
                   (((imgbytes[i + 1] & 1) << 6) & 0x40) | \
                   (((imgbytes[i + 2] & 1) << 5) & 0x20) | \
                   (((imgbytes[i + 3] & 1) << 4) & 0x10) | \
                   (((imgbytes[i + 4] & 1) << 3) & 0x08) | \
                   (((imgbytes[i + 5] & 1) << 2) & 0x04) | \
                   (((imgbytes[i + 6] & 1) << 1) & 0x02) | \
                   (((imgbytes[i + 7] & 1) << 0) & 0x01)

            imgnewbytes0[pointer] = chr(temp & 0xFF)

            pointer += 1
            i += 8

        pointer = 0
        i = 0
        loop_len = len(imgbytes)
        while i < loop_len:
            temp = (((imgbytes[i + 0] & 2) << 6) & 0x80) | \
                   (((imgbytes[i + 1] & 2) << 5) & 0x40) | \
                   (((imgbytes[i + 2] & 2) << 4) & 0x20) | \
                   (((imgbytes[i + 3] & 2) << 3) & 0x10) | \
                   (((imgbytes[i + 4] & 2) << 2) & 0x08) | \
                   (((imgbytes[i + 5] & 2) << 1) & 0x04) | \
                   (((imgbytes[i + 6] & 2) << 0) & 0x02) | \
                   (((imgbytes[i + 7] & 2) >> 1) & 0x01)

            imgnewbytes1[pointer] = chr(temp & 0xFF)

            pointer += 1
            i += 8
        return (imgnewbytes1, imgnewbytes0)