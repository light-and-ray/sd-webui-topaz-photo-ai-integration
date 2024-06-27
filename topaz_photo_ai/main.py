import os
from pathlib import Path
from PIL import Image
from modules import shared
from topaz_photo_ai.tools import runTopaz

# --overwrite --upscale scale=4 height=2048 width=2048 minor_denoise=100 minor_deblur=100
# model="High Fidelity V2" --sharpen strength=100 --denoise strength=100 minor_deblur=100
# original_detail=100 --quality 100 --compression 10 --tiff-compression "lzw" "{temp_image}"'



def upscale(img: Image.Image, scale: int) -> Image.Image:
    return runTopaz(img, '--upscale', f'scale={scale}')

def sharpen(img: Image.Image, percent: int) -> Image.Image:
    return runTopaz(img, '--sharpen', f'strength={percent}')
