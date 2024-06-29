from PIL import Image
from dataclasses import dataclass
from topaz_photo_ai.tools import runTopaz



def simpleUpscale(img: Image.Image, scale: int) -> Image.Image:
    return runTopaz(img, '--upscale', f'scale={scale}', '--face_recovery', 'enabled=false')



DENOISE_MODELS = ["Automatic", "Normal", "Strong", "Extreme"]

def fillModelForDenoise(args, model):
    if model == "Normal":
        args.append("model=Low Light Beta")
    elif model == "Strong":
        args.append("model=Severe Noise")
    elif model == "Extreme":
        args.append("model=Severe Noise Beta")

def fillParams1ForDenoise(args, strength):
    args.append(f"param1_normalv2={strength/100}")
    args.append(f"param1_strongv2={strength/100}")
    args.append(f"param1={strength/100}")

def fillParams2ForDenoise(args, minor_deblur):
    args.append(f"param2_normalv2={minor_deblur/100}")
    args.append(f"param2_strongv2={minor_deblur/100}")
    args.append(f"param2={minor_deblur/100}")



class DenoiseOptions:
    model: str = None
    strength: int = None
    minor_denoise: int = None
    original_detail: int = None



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
    denoise: DenoiseOptions = None
    sharpen: SharpenOptions = None



def argsDictToOptions(args: dict) -> TopazPhotoAIOptions:
    o = TopazPhotoAIOptions()

    if args['d_enable']:
        denoise = DenoiseOptions()
        denoise.model = args['d_model']
        denoise.strength = args['d_strength']
        denoise.minor_denoise = args['d_minor_denoise']
        denoise.original_detail = args['d_original_detail']
        o.denoise = denoise

    if args['s_enable']:
        sharpen = SharpenOptions()
        sharpen.model = args['s_model']
        sharpen.strength = args['s_strength']
        sharpen.minor_denoise = args['s_minor_denoise']
        o.sharpen = sharpen

    return o


def processTopazPhotoAI(img: Image.Image, o: TopazPhotoAIOptions):
    args = []

    args.append('--denoise')
    if o.denoise:
        if o.denoise.model != "Automatic":
            fillModelForDenoise(args, o.denoise.model)
        if o.denoise.strength != -1:
            fillParams1ForDenoise(args, o.denoise.strength)
        if o.denoise.minor_denoise != -1:
            fillParams2ForDenoise(args, o.denoise.minor_denoise)
        if o.denoise.original_detail != -1:
            args.append(f'recover_detail={o.denoise.original_detail/100}')
    else:
        args.append('enabled=false')

    args.append('--sharpen')
    if o.sharpen:
        if o.sharpen.model != "Automatic":
            fillArgsForSharpenModel(args, o.sharpen.model)
        if o.sharpen.strength != -1:
            args.append(f'param2={o.sharpen.strength/100}')
        if o.sharpen.minor_denoise != -1:
            args.append(f'param1={o.sharpen.minor_denoise/100}')
    else:
        args.append('enabled=false')

    args.append('--upscale')
    args.append('enabled=false')

    args.append('--face_recovery')
    args.append('enabled=false')

    return runTopaz(img, *args)

