import bpy
from bpy.types import Panel
from ...pil_to_image import *
from ...prompt_engineering import *
from ...operators.upscale import Upscale
from ...absolute_path import REAL_ESRGAN_WEIGHTS_PATH
from ..space_types import SPACE_TYPES
import os
import webbrowser

class OpenRealESRGANDownload(bpy.types.Operator):
    bl_idname = "stable_diffusion.open_realesrgan_download"
    bl_label = "Download Weights from GitHub"
    bl_description = ("Opens to the latest release of Real-ESRGAN, where the weights can be downloaded.")
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        webbrowser.open("https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.3.0")
        return {"FINISHED"}

class OpenRealESRGANWeightsDirectory(bpy.types.Operator):
    bl_idname = "stable_diffusion.open_realesrgan_weights_directory"
    bl_label = "Open Target Directory"
    bl_description = ("Opens the directory that should contain the 'realesr-general-x4v3.pth' file")
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        path = os.path.dirname(REAL_ESRGAN_WEIGHTS_PATH)
        if not os.path.exists(path):
            os.mkdir(path)
        webbrowser.open(f"file:///{os.path.realpath(path)}")
        
        return {"FINISHED"}

def upscaling_panels():
    for space_type in SPACE_TYPES:
        class UpscalingPanel(Panel):
            """Panel for AI Upscaling"""
            bl_label = "AI Upscaling"
            bl_category = "Dream"
            bl_idname = f"DREAM_PT_dream_upscaling_panel_{space_type}"
            bl_space_type = space_type
            bl_region_type = 'UI'
            bl_options = {'DEFAULT_CLOSED'}

            @classmethod
            def poll(self, context):
                if self.bl_space_type == 'NODE_EDITOR':
                    return context.area.ui_type == "ShaderNodeTree" or context.area.ui_type == "CompositorNodeTree"
                else:
                    return True

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True
                if not os.path.exists(REAL_ESRGAN_WEIGHTS_PATH):
                    layout.label(text="Real-ESRGAN model weights not installed.")
                    layout.label(text="1. Download the file 'realesr-general-x4v3.pth' from GitHub")
                    layout.operator(OpenRealESRGANDownload.bl_idname, icon="URL")
                    layout.label(text="2. Place it in the weights folder with the name 'realesr-general-x4v3.pth'")
                    layout.operator(OpenRealESRGANWeightsDirectory.bl_idname, icon="FOLDER_REDIRECT")
                layout = layout.column()
                layout.enabled = os.path.exists(REAL_ESRGAN_WEIGHTS_PATH)
                layout.prop(context.scene, "dream_textures_upscale_outscale")
                layout.prop(context.scene, "dream_textures_upscale_full_precision")
                if not context.scene.dream_textures_upscale_full_precision:
                    box = layout.box()
                    box.label(text="Note: Some GPUs do not support mixed precision math", icon="ERROR")
                    box.label(text="If you encounter an error, enable full precision.")
                if context.scene.dream_textures_info != "":
                    layout.label(text=context.scene.dream_textures_info, icon="INFO")
                else:
                    layout.operator(Upscale.bl_idname, icon="FULLSCREEN_ENTER")
        
        UpscalingPanel.__name__ = f"DREAM_PT_dream_troubleshooting_panel_{space_type}"
        yield UpscalingPanel