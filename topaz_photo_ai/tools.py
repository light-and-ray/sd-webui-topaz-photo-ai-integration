import subprocess, os
from tempfile import TemporaryDirectory
from PIL import Image
import gradio as gr
from modules import shared, script_callbacks


def on_ui_settings():
    shared.opts.add_option(
        "topaz_photo_ai_exe",
        shared.OptionInfo(
            "",
            "Path to topaz's cli executable: tpai.exe or a script-wrapper of it",
            gr.Textbox,
            section=('upscaling', "Upscaling")
        )
    )

script_callbacks.on_ui_settings(on_ui_settings)


def getTopazAIEXE():
    exe = shared.opts.data.get("topaz_photo_ai_exe", "")
    if not exe or not os.path.exists(exe):
        raise Exception(f'Topaz executable file is not found. Please set it up in Settings/Upscaling')
    return exe


def runTopaz_(*cmd):
    cmd = [getTopazAIEXE()] + list(cmd)
    cmd = [str(v) for v in cmd]
    print(' '.join(f"'{v}'" if ' ' in v else v for v in cmd))
    rc = subprocess.run(cmd).returncode
    if rc != 0:
        if rc == 2:
            raise Exception('Maybe another instance of Topaz exists. Return code = 2')
        if rc == 1:
            raise Exception('Return code = 1 - Partial Success (e.g., some files failed)')
        if rc in (-1, 255):
            raise Exception('Return code = -1 (255) - No valid files passed.')
        if rc in (-2, 254):
            raise Exception('Return code = -2 (254) - Invalid log token. Open the app normally to login.')
        if rc in (-3, 253):
            raise Exception('Return code = -3 (253) - An invalid argument was found.')
        raise Exception(f'Topaz exited with code {rc} (Unknown code)')


def runTopaz(img: Image.Image, *cmd) -> Image.Image:
    tmpInDir = TemporaryDirectory()
    tmpOutDir = TemporaryDirectory()
    try:
        fileIn = os.path.join(tmpInDir.name, 'file.jpg')
        fileOut = os.path.join(tmpOutDir.name, 'file.jpg')
        img.convert('RGB').save(fileIn, quality=95)
        runTopaz_('--output', tmpOutDir.name, '--override', *cmd, fileIn)
        if not os.path.exists(fileOut):
            raise Exception("Topaz didn't process any image")
        return Image.open(fileOut)
    finally:
        try:
            tmpInDir.cleanup()
            tmpOutDir.cleanup()
        except:
            pass
