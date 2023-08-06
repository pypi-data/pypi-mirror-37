# -*- coding: utf-8 -*-
from image2char.core.scanner import ImageScanner
from PIL import Image
from io import BytesIO
import requests


def get_scanner(density, scale):
    scanner = ImageScanner()
    scanner.set_density(density)
    scanner.set_scale(scale)
    return scanner


def to_chars(img, density=0.2, scale=2, reversed=False, char_list=None):
    scanner = get_scanner(density, scale)
    scanner.scan(img, reversed, char_list)
    return scanner.get_result()


def from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image


def from_path(path):
    return Image.open(path)
