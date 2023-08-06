# -*- coding: utf-8 -*-
import logging


class Processor(object):
    def __init__(self):
        self.char_list = r'@%B8&WM#*gkhabdpqdfwmsojlzcv'
        self.char_list += r'unxr/\{}()Il1i!;:[]<>?|+~-_,"\'. '
        logging.debug(self.char_list)
        return

    def gray(self, rgb):
        r, g, b = rgb
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        return gray

    def weight(self, weight_x, weight_y):
        # default weight function
        return 1

    def process(self, chop):
        num = 0
        size_y, size_x = chop.size
        for y in range(size_y):
            for x in range(size_x):
                # may add weight
                weight_y = min(y, size_y-y)*2/size_y
                weight_x = min(x, size_x-x)*2/size_x
                weight = self.weight(weight_x, weight_y)
                num += self.gray(chop.getpixel((y, x))) * weight
        return int(num / (size_y * size_x))

    def map(self, chop, reversed, char_list, color_range=(0, 255)):
        if char_list is None:
            char_list = self.char_list

        value = self.process(chop)
        color_min = min(color_range)
        color_max = max(color_range)
        scale = value / (color_max - color_min)
        if reversed:
            scale = 1 - scale
        position = int((len(char_list)-1) * scale + 0.5)
        return char_list[position]

    pass
