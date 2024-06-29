from PIL import Image
from dataclasses import dataclass
from topaz_photo_ai.tools import runTopaz



def simpleUpscale(img: Image.Image, scale: int) -> Image.Image:
    return runTopaz(img, '--upscale', f'scale={scale}', '--face_recovery', 'enabled=false')




SHARPEN_MODELS = ["Automatic", "Standard", "Strong", "Lens blur", "Motion blur"]

def fillArgsForSharpenModel(args, model):
    if model == "Standard":
        args.append("model=Sharpen Standard v2")
    elif model == "Strong":
        args.append("model=Sharpen Strong")
    elif model == "Lens blur":
        args.append("model=Sharpen Standard")
        args.append("isLens=true")
    elif model == "Motion blur":
        args.append("model=Sharpen Standard")
        args.append("isLens=false")


class SharpenOptions:
    model: str = None
    strength: int = None
    minor_denoise: int = None


@dataclass
class TopazPhotoAIOptions:
    sharpen: SharpenOptions = None



def processTopazPhotoAI(img: Image.Image, o: TopazPhotoAIOptions):
    args = []
    args.append('--sharpen')
    if o.sharpen:
        if o.sharpen.model != "Automatic":
            fillArgsForSharpenModel(args, o.sharpen.model)
        if o.sharpen.strength != -1:
            args.append(f'param2={o.sharpen.strength}')
        if o.sharpen.minor_denoise != -1:
            args.append(f'param1={o.sharpen.minor_denoise}')
    else:
        args.append('enabled=false')

    args.append('--upscale')
    args.append('enabled=false')

    args.extend(['--face_recovery', 'enabled=false'])

    return runTopaz(img, *args)

