import gradio as gr
import copy
from modules import scripts_postprocessing
from modules.ui_components import InputAccordion
from topaz_photo_ai.main import TopazPhotoAIOptions, SharpenOptions, processTopazPhotoAI, SHARPEN_MODELS


class TopazExtras(scripts_postprocessing.ScriptPostprocessing):
    name = "Topaz Photo AI"
    order = 1020

    def sharpenUI(self):
        with InputAccordion(False, label='Sharpen') as enable:
            model = gr.Radio(value="Automatic", choices=SHARPEN_MODELS, label="Model")
            strength = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Strength", info="-1 means automatic")
            minor_denoise = gr.Slider(value=-1, minimum=-1, maximum=100, step=1, label="Minor denoise", info="-1 means automatic")

        args = {
            's_enable': enable,
            's_model' : model,
            's_strength' : strength,
            's_minor_denoise' : minor_denoise,
        }
        return args


    def ui(self):
        with InputAccordion(False, label=self.name) as enable:
            sharpenArgs = self.sharpenUI()

        args = {
            'enable': enable,
        }
        args.update(sharpenArgs)
        return args

    # def process_firstpass(self, pp: scripts_postprocessing.PostprocessedImage, **args):
    #     pp.shared.target_width = pp.image.width * 2 ** (args['scale'] + 1)
    #     pp.shared.target_height = pp.image.height * 2 ** (args['scale'] + 1)

    def process(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        if args['enable'] == False:
            return

        o = TopazPhotoAIOptions()
        if args['s_enable']:
            sharpen = SharpenOptions()
            sharpen.model = args['s_model']
            sharpen.strength = args['s_strength']
            sharpen.minor_denoise = args['s_minor_denoise']
            o.sharpen = sharpen

        pp.image = processTopazPhotoAI(pp.image, o)

        info = copy.copy(args)
        del info['enable']
        pp.info[self.name] = str(info)

