import os
import random
import json
from pathlib import Path

class PromptSaveNode:
    """保存反推提示词节点
    
    用于接收来自反推工作流的提示词字符串，并将其保存到文件中。
    可以与任何产生提示词字符串的节点配合使用，包括各种反推节点。
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "save_path": ("STRING", {"default": "E:/Project1/Wildcards-Generator/prompts"}),
                "save_mode": (["single_file", "multiple_files"], {"default": "single_file"}),
            },
            "optional": {
                "file_name": ("STRING", {"default": "prompts.txt"}),
                "image_name": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_prompt"
    OUTPUT_NODE = True
    CATEGORY = "提示词"
    
    def save_prompt(self, prompt, save_path, save_mode, file_name="prompts.txt", image_name=""):
        """保存提示词到文件
        
        参数:
        - prompt: 要保存的提示词字符串，通常来自反推节点的输出
        - save_path: 保存文件的目标路径
        - save_mode: 保存模式，single_file或multiple_files
        - file_name: 保存的文件名（仅在single_file模式下有效）
        - image_name: 图片名称（仅在multiple_files模式下有效，用于生成文件名）
        """
        try:
            # 确保保存路径存在
            Path(save_path).mkdir(parents=True, exist_ok=True)
            
            if save_mode == "multiple_files":
                # 为每张图片创建单独的txt文件
                if not image_name:
                    # 如果没有提供图片名称，生成一个随机名称
                    image_name = f"prompt_{random.randint(1000, 9999)}"
                file_path = os.path.join(save_path, f"{image_name}.txt")
            else:
                # 汇总到同一txt文件
                file_path = os.path.join(save_path, file_name)
            
            # 写入提示词
            with open(file_path, "a" if save_mode == "single_file" else "w", encoding="utf-8") as f:
                f.write(prompt + "\n")
            
            return {
                "ui": {
                    "text": [f"提示词已保存到: {file_path}"]
                }
            }
        except Exception as e:
            return {
                "ui": {
                    "text": [f"保存失败: {str(e)}"]
                }
            }

class RandomWildcardNode:
    """随机提示词抽取节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wildcard_file": ("STRING", {"default": "E:/Project1/Wildcards-Generator/wildcards.txt"}),
                "num_prompts": ("INT", {"default": 1, "min": 1, "max": 100}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "fixed_prompt": ("STRING", {"default": "", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("random_prompt",)
    FUNCTION = "get_random_prompt"
    CATEGORY = "提示词"
    
    def get_random_prompt(self, wildcard_file, num_prompts, seed, fixed_prompt=""):
        """从wildcard文件中随机抽取提示词，并与固定提示词合并"""
        try:
            # 设置随机种子
            if seed > 0:
                random.seed(seed)
            
            # 读取wildcard文件
            with open(wildcard_file, "r", encoding="utf-8") as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            if not prompts:
                return (fixed_prompt,)
            
            # 随机抽取提示词
            random_prompts = random.choices(prompts, k=num_prompts)
            random_result = "\n".join(random_prompts)
            
            # 合并固定提示词和随机提示词
            if fixed_prompt:
                # 如果有多个随机提示词，每个都添加固定前缀
                if num_prompts > 1:
                    combined_prompts = []
                    for prompt in random_prompts:
                        combined_prompts.append(f"{fixed_prompt}, {prompt}")
                    result = "\n".join(combined_prompts)
                else:
                    # 单个随机提示词，直接合并
                    result = f"{fixed_prompt}, {random_result}"
            else:
                # 没有固定提示词，直接返回随机提示词
                result = random_result
            
            return (result,)
        except Exception as e:
            print(f"读取wildcard文件失败: {str(e)}")
            return ("",)

# 节点映射
NODE_CLASS_MAPPINGS = {
    "PromptSaveNode": PromptSaveNode,
    "RandomWildcardNode": RandomWildcardNode
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptSaveNode": "保存反推提示词",
    "RandomWildcardNode": "随机抽取提示词"
}
