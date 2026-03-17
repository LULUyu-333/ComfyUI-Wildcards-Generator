# 文件路径: custom_nodes/ComfyUI_ImageSequenceLoader/__init__.py

# 导入你的 Python 节点类
from .image_sequence_node import ImageSequenceLoader

# 告诉 ComfyUI 你的 JS 文件在哪里
WEB_DIRECTORY = "./web"

# 将你的节点类添加到 NODE_CLASS_MAPPINGS 中
NODE_CLASS_MAPPINGS = {
    "ImageSequenceLoader": ImageSequenceLoader,
}

# 可选：定义更友好的名称用于日志
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSequenceLoader": "🖼️ 图像序列加载器"
}

print("Loaded 🖼️ ImageSequenceLoader node.")
