# -*- coding: utf-8 -*-
import logging
from image2char.core.processor import Processor


class ImageScanner(object):
    '''
    use computer location: [|Y][——X]
    '''

    def __init__(self):
        self.density = 0
        self.scale = 2
        self.processor = Processor()
        self.result = [[]]
        self.width = 0
        self.height = 0
        self.encoding = 'utf-8'
        return

    def set_density(self, density):
        self.density = density
        return

    def set_scale(self, scale):
        self.scale = scale
        return

    def set_encoding(self, encoding):
        self.encoding = encoding
        return

    def _cut(self, img, start_x, start_y, end_x, end_y):
        return img.crop((start_x, start_y, end_x, end_y))

    def _calculate(self, origin_size):
        origin_x, origin_y = origin_size
        width = self.density_map(origin_x)
        scan_step_x = origin_x / width
        scan_step_y = scan_step_x * self.scale
        height = width / self.scale * origin_y / origin_x

        scan_step_x = self.order(scan_step_x)
        scan_step_y = self.order(scan_step_y)
        self.height = self.order(height)
        self.width = self.order(width)
        return scan_step_x, scan_step_y

    def density_map(self, origin_x):
        density_x = (origin_x - 1) * self.density
        final_x = density_x * self.density + 1
        return int(final_x)

    def order(self, num):
        return int(num + 0.5)

    def scan(self, img, reversed, char_list):
        logging.debug('origin_size: (%d, %d)' % img.size)

        scan_step_x, scan_step_y = self._calculate(img.size)
        logging.debug('scan_step: (%d, %d)' % (scan_step_x, scan_step_y))
        logging.debug('processed: (%d, %d)' % (self.width, self.height))

        self.result = [([''] * self.width) for i in range(self.height)]
        for y in range(self.height):
            start_y = y * scan_step_y
            end_y = start_y + scan_step_y
            for x in range(self.width):
                start_x = x * scan_step_x
                end_x = start_x + scan_step_x
                chop = self._cut(img, start_x, start_y, end_x, end_y)
                self.result[y][x] = self.processor.map(
                    chop, reversed=reversed, char_list=char_list)
        
        logging.debug('end at: (%d, %d)' % (end_x, end_y))
        return

    def get_result(self):
        return self.result

    def print_result(self):
        matrix = self.get_result()
        for i in range(len(matrix)):
            print(''.join(matrix[i]))

    pass
