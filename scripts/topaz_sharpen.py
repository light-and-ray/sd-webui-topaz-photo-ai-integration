# from dataclasses import dataclass
# from modules.upscaler import Upscaler, UpscalerData
# from topaz_photo_ai.main import sharpen


# @dataclass
# class Fields:
#     percent: int

# data = [
#     Fields(100),
#     Fields(85),
#     Fields(70),
#     Fields(55),
#     Fields(40),
# ]

# class BaseClass(Upscaler):
#     def __init__(self, dirname, fields: Fields = None):
#         if fields is None:
#             self.scalers = []
#             return
#         self.name = "Topaz"
#         self.fields = fields
#         self.scalers = [UpscalerData(f'Topaz Photo AI - Sharpen 1x {self.fields.percent}', None, self, 1)]
#         super().__init__()

#     def do_upscale(self, img, selected_model):
#         return sharpen(img, self.fields.percent)

# class Class0(BaseClass, Upscaler):
#     def __init__(self, dirname):
#         super().__init__(dirname, data[0])
# class Class1(BaseClass, Upscaler):
#     def __init__(self, dirname):
#         super().__init__(dirname, data[1])
# class Class2(BaseClass, Upscaler):
#     def __init__(self, dirname):
#         super().__init__(dirname, data[2])
# class Class3(BaseClass, Upscaler):
#     def __init__(self, dirname):
#         super().__init__(dirname, data[3])
# class Class4(BaseClass, Upscaler):
#     def __init__(self, dirname):
#         super().__init__(dirname, data[4])
