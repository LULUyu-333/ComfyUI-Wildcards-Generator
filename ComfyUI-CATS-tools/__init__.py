# 导入所有节点类
from .nodes import StringSaveNode, RandomWildcardNode, ImageSequenceLoader, SequentialWildcardNode, 数值分割节点, ReversePromptSaveNode, aistudynow_QwenVL

# 配置web目录
WEB_DIRECTORY = "./web"

# 注册所有节点
NODE_CLASS_MAPPINGS = {
    "StringSaveNode": StringSaveNode,
    "RandomWildcardNode": RandomWildcardNode,
    "SequentialWildcardNode": SequentialWildcardNode,
    "ImageSequenceLoader": ImageSequenceLoader,
    "数值分割节点": 数值分割节点,
    "ReversePromptSaveNode": ReversePromptSaveNode,
    "aistudynow_QwenVL": aistudynow_QwenVL,
}

# 定义友好的显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "StringSaveNode": "🔤 字符串保存节点",
    "RandomWildcardNode": "🎲 随机抽取提示词",
    "SequentialWildcardNode": "📋 顺序提取提示词",
    "ImageSequenceLoader": "🖼️ 图像序列加载器",
    "数值分割节点": "🔢 数值分割节点",
    "ReversePromptSaveNode": "🔄 反推提示词保存",
    "aistudynow_QwenVL": "QwenVL (CATS)",
}

print("Loaded 🐱 CATS (Creative Assistant Tools Suite) nodes.")
