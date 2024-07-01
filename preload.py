import os
from modules import paths


def preload(parser):
    parser.add_argument("--topaz-photo-ai-exe", type=str,
        help="Path to topaz's cli executable: tpai.exe or a script-wrapper of it")
