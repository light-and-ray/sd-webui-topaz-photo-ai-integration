import gradio as gr
import copy
from modules import scripts_postprocessing
from modules.ui_components import InputAccordion
from topaz_photo_ai.main import (TopazPhotoAIOptions, SharpenOptions, processTopazPhotoAI, SHARPEN_MODELS, DENOISE_MODELS,
    DenoiseOptions,
)


class TopazExtras(scripts_postprocessing.ScriptPostprocessing):
    name = "Topaz Photo AI"
    order = 1020

    def denoiseUI(self):
        with InputAccordion(False, label='Denoise') as enable:
            model = gr.Radio(value="Automatic", choices=DENOISE_MODELS, label="Model")
            with gr.Row():
                strength = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Strength", info="-1 means automatic")
                minor_denoise = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Minor denoise", info="-1 means automatic")
                original_detail = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Original detail", info="-1 means automatic")

        args = {
            'd_enable': enable,
            'd_model' : model,
            'd_strength' : strength,
            'd_minor_denoise' : minor_denoise,
            'd_original_detail' : original_detail,
        }
        return args


    def sharpenUI(self):
        with InputAccordion(False, label='Sharpen') as enable:
            model = gr.Radio(value="Automatic", choices=SHARPEN_MODELS, label="Model")
            with gr.Row():
                strength = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Strength", info="-1 means automatic")
                minor_denoise = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Minor denoise", info="-1 means automatic")

        model.change(fn=lambda x: gr.update(visible=(x != "Strong")), inputs=[model], outputs=[minor_denoise], show_progress=False)

        args = {
            's_enable': enable,
            's_model' : model,
            's_strength' : strength,
            's_minor_denoise' : minor_denoise,
        }
        return args


    def ui(self):
        with InputAccordion(False, label=self.name) as enable:
            with gr.Column():
                denoiseArgs = self.denoiseUI()
                sharpenArgs = self.sharpenUI()
            gr.Markdown('(Models are tested in version 3.0.4)')

        args = {
            'enable': enable,
        }
        args.update(denoiseArgs)
        args.update(sharpenArgs)
        return args




    def process(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        if args['enable'] == False:
            return

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

        pp.image = processTopazPhotoAI(pp.image, o)

        info = copy.copy(args)
        del info['enable']
        keysForDel = set()
        for key, value in info.items():
            if not info['d_enable'] and key.startswith('d_'):
                keysForDel.add(key)
            if not info['s_enable'] and key.startswith('s_'):
                keysForDel.add(key)
            if value in (-1, 'Automatic'):
                keysForDel.add(key)
        for key in keysForDel:
            del info[key]
        pp.info[self.name] = str(info)


    # def process_firstpass(self, pp: scripts_postprocessing.PostprocessedImage, **args):
    #     pp.shared.target_width = pp.image.width * 2 ** (args['scale'] + 1)
    #     pp.shared.target_height = pp.image.height * 2 ** (args['scale'] + 1)

