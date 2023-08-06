# -*- coding: utf-8 -*-
from image2char.core.scanner import ImageScanner


def get_scanner(density, scale):
    scanner = ImageScanner()
    scanner.set_density(density)
    scanner.set_scale(scale)
    return scanner


def to_chars(img, density=0.2, scale=2, reversed=False, char_list=None):
    scanner = get_scanner(density, scale)
    scanner.scan(img, reversed, char_list)
    return scanner.get_result()
