import os
import random
import json
from pathlib import Path
import torch
from PIL import Image
import numpy as np

class StringSaveNode:
    """字符串保存节点
    
    用于接收任何字符串，在节点下方展示内容，并将其保存到txt文档中。
    支持选择保存模式：单次保存或汇总保存为wildcards格式。
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING", {"multiline": True, "default": "", "placeholder": "在此输入或连接字符串..."}),
                "save_path": ("STRING", {"default": "E:/Project1/Wildcards-Generator/prompts", "vfile": {".": {"accept": ".", "save": True}}}),
                "file_name": ("STRING", {"default": "wildcards.txt"}),
                "save_mode": (["single_file", "wildcards_format"], {"default": "wildcards_format"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("文本",)
    FUNCTION = "save_string"
    OUTPUT_NODE = True
    CATEGORY = "🐱 CATS"
    
    def save_string(self, 文本, save_path, file_name, save_mode):
        """保存字符串到文件，并展示内容
        
        参数:
        - 文本: 要保存的字符串或复杂类型
        - save_path: 保存文件的目标路径
        - file_name: 保存的文件名
        - save_mode: 保存模式，single_file或wildcards_format
        
        返回:
        - 文本: 返回输入字符串，保持数据流
        """
        try:
            # 类型检查和转换
            input_type = type(文本).__name__
            
            # 处理不同类型的输入
            if isinstance(文本, str):
                # 纯字符串，直接使用
                string_text = 文本.strip()
                conversion_info = f"纯字符串类型，直接使用"
            elif isinstance(文本, dict):
                # 字典类型，尝试提取提示词字段
                conversion_info = f"字典类型，尝试提取提示词字段"
                # 常见的提示词字段名
                prompt_keys = ["output", "prompt", "text", "result", "content", "response"]
                for key in prompt_keys:
                    if key in 文本:
                        string_text = str(文本[key]).strip()
                        conversion_info += f"，提取字段: {key}"
                        break
                else:
                    # 没有找到匹配的字段，尝试将整个字典转换为字符串
                    string_text = str(文本).strip()
                    conversion_info += f"，未找到匹配字段，转换为字符串"
            elif isinstance(文本, (list, tuple)):
                # 列表或元组类型，处理第一个元素
                conversion_info = f"列表/元组类型，处理第一个元素"
                if 文本:
                    first_item = 文本[0]
                    if isinstance(first_item, str):
                        string_text = first_item.strip()
                        conversion_info += f"，第一个元素为字符串"
                    elif isinstance(first_item, dict):
                        # 处理第一个元素为字典的情况
                        prompt_keys = ["output", "prompt", "text", "result", "content", "response"]
                        for key in prompt_keys:
                            if key in first_item:
                                string_text = str(first_item[key]).strip()
                                conversion_info += f"，提取第一个元素的{key}字段"
                                break
                        else:
                            string_text = str(first_item).strip()
                            conversion_info += f"，未找到匹配字段，转换第一个元素为字符串"
                    else:
                        string_text = str(first_item).strip()
                        conversion_info += f"，转换第一个元素为字符串"
                else:
                    string_text = ""
                    conversion_info += f"，列表为空"
            else:
                # 其他类型，尝试转换为字符串
                string_text = str(文本).strip()
                conversion_info = f"{input_type}类型，转换为字符串"
            
            # 确保转换后的字符串不为空
            if not string_text:
                return {
                    "ui": {
                        "text": [
                            "转换后的字符串为空",
                            f"原始输入类型: {input_type}",
                            f"转换信息: {conversion_info}",
                            "请检查输入或连接的节点"
                        ]
                    },
                    "result": ("",)
                }
            
            # 确保保存路径存在
            Path(save_path).mkdir(parents=True, exist_ok=True)
            
            # 构建基础文件名（不含扩展名）
            base_name, _ = os.path.splitext(file_name)  # 忽略输入的扩展名
            ext = ".txt"  # 强制使用.txt扩展名
            
            file_path = ""
            
            if save_mode == "single_file":
                # 单文件模式：每次执行保存为新文件，自动添加累计数字
                counter = 0
                while True:
                    if counter == 0:
                        temp_file_path = os.path.join(save_path, f"{base_name}{ext}")
                    else:
                        temp_file_path = os.path.join(save_path, f"{base_name}{counter}{ext}")
                    
                    if not os.path.exists(temp_file_path):
                        file_path = temp_file_path
                        break
                    counter += 1
                
                # 保存文件
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(string_text + "\n")
                
                message = f"字符串已保存到新文件"
                saved = True
            else:
                # wildcards_format模式：每行一组提示词，每次执行的文本为一组
                file_path = os.path.join(save_path, f"{base_name}{ext}")
                
                # 直接追加到文件，每行一组提示词
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(string_text + "\n")
                
                message = f"提示词组已添加到wildcards文件"
                saved = True
            
            # 准备UI输出，确保文本显示在节点下方
            ui_output = {
                "text": [
                    string_text,
                    "",
                    f"原始输入类型: {input_type}",
                    f"转换信息: {conversion_info}",
                    message,
                    f"文件: {file_path}",
                    f"大小: {os.path.getsize(file_path)} 字节"
                ]
            }
            
            return {
                "ui": ui_output,
                "result": (文本,)
            }
        except Exception as e:
            error_msg = f"操作失败: {str(e)}"
            return {
                "ui": {
                    "text": [
                        error_msg,
                        f"错误: {type(e).__name__}",
                        f"输入类型: {type(文本).__name__}",
                        f"输入内容: {str(文本)[:100]}..."
                    ]
                },
                "result": ("",)
            }

class RandomWildcardNode:
    """随机提示词抽取节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wildcard_file": ("STRING", {"default": "", "vfile": {".": {"accept": ".txt"}}}),
                "num_prompts": ("INT", {"default": 1, "min": 1, "max": 100}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "fixed_prompt": ("STRING", {"default": "", "multiline": True, "placeholder": "在此输入固定提示词..."}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("random_prompt",)
    FUNCTION = "get_random_prompt"
    CATEGORY = "🐱 CATS"
    
    def get_random_prompt(self, wildcard_file, num_prompts, seed, fixed_prompt=""):
        """从wildcard文件中随机抽取提示词，并与固定提示词合并
        
        参数:
        - wildcard_file: wildcards文件路径
        - num_prompts: 要抽取的提示词数量
        - seed: 随机种子，0表示使用随机种子
        - fixed_prompt: 固定提示词，用于添加前缀
        
        返回:
        - 合并后的提示词字符串
        """
        try:
            # 验证文件路径
            if not wildcard_file or not os.path.exists(wildcard_file):
                return (f"错误: 文件不存在或路径为空: {wildcard_file}",)
            
            if not os.path.isfile(wildcard_file):
                return (f"错误: 不是有效的文件: {wildcard_file}",)
            
            # 设置随机种子
            if seed > 0:
                random.seed(seed)
            else:
                # 使用基于时间的随机种子
                import time
                random.seed(time.time())
            
            # 读取wildcard文件
            with open(wildcard_file, "r", encoding="utf-8") as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            if not prompts:
                return (f"警告: 文件中没有有效的提示词: {wildcard_file}",)
            
            # 随机抽取提示词
            random_prompts = random.choices(prompts, k=num_prompts)
            
            # 合并固定提示词和随机提示词
            if fixed_prompt:
                # 去除固定提示词两端的空格
                fixed_prompt = fixed_prompt.strip()
                if fixed_prompt:
                    # 如果有多个随机提示词，每个都添加固定前缀
                    if num_prompts > 1:
                        combined_prompts = []
                        for prompt in random_prompts:
                            combined_prompts.append(f"{fixed_prompt}, {prompt}")
                        result = "\n".join(combined_prompts)
                    else:
                        # 单个随机提示词，直接合并
                        result = f"{fixed_prompt}, {random_prompts[0]}"
                else:
                    # 固定提示词为空，直接返回随机提示词
                    result = "\n".join(random_prompts)
            else:
                # 没有固定提示词，直接返回随机提示词
                result = "\n".join(random_prompts)
            
            return (result,)
        except FileNotFoundError:
            return (f"错误: 文件未找到: {wildcard_file}",)
        except PermissionError:
            return (f"错误: 没有权限读取文件: {wildcard_file}",)
        except Exception as e:
            error_msg = f"错误: 读取文件失败: {str(e)}"
            print(error_msg)
            return (error_msg,)


class SequentialWildcardNode:
    """按顺序提取提示词节点
    
    从wildcards文件中按顺序提取提示词，根据trigger值切换到对应索引的提示词。
    支持添加固定前缀，可连接计数节点实现自动切换。
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wildcard_file": ("STRING", {"default": "", "vfile": {".": {"accept": ".txt"}}}),
                "trigger": ("INT", {"default": 0, "min": 0}),  # 触发值，用于确定当前索引
                "fixed_prompt": ("STRING", {"default": "", "multiline": True, "placeholder": "在此输入固定提示词..."}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("prompt", "current_index", "file_info")
    FUNCTION = "get_next_prompt"
    CATEGORY = "🐱 CATS"
    
    def get_next_prompt(self, wildcard_file, trigger, fixed_prompt=""):
        """从wildcard文件中按顺序提取提示词
        
        参数:
        - wildcard_file: wildcards文件路径
        - trigger: 触发值，用于确定当前索引，每次递增1即可切换到下一个提示词
        - fixed_prompt: 固定提示词，用于添加前缀
        
        返回:
        - prompt: 合并后的提示词
        - current_index: 当前提取的索引
        - file_info: 文件信息
        """
        try:
            # 验证文件路径
            if not wildcard_file or not os.path.exists(wildcard_file):
                return (f"错误: 文件不存在或路径为空: {wildcard_file}", 0, "")
            
            if not os.path.isfile(wildcard_file):
                return (f"错误: 不是有效的文件: {wildcard_file}", 0, "")
            
            # 读取文件内容
            with open(wildcard_file, "r", encoding="utf-8") as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            if not prompts:
                return (f"警告: 文件中没有有效的提示词: {wildcard_file}", 0, "")
            
            # 根据trigger值计算当前索引，实现循环
            current_index = trigger % len(prompts)
            
            # 获取当前提示词
            current_prompt = prompts[current_index]
            
            # 合并固定提示词和当前提示词
            if fixed_prompt:
                # 去除固定提示词两端的空格
                fixed_prompt = fixed_prompt.strip()
                if fixed_prompt:
                    result = f"{fixed_prompt}, {current_prompt}"
                else:
                    result = current_prompt
            else:
                result = current_prompt
            
            # 准备文件信息
            file_info = f"文件: {os.path.basename(wildcard_file)} | 总数: {len(prompts)} | 当前: {current_index + 1}"
            
            return (result, current_index, file_info)
        except FileNotFoundError:
            return (f"错误: 文件未找到: {wildcard_file}", 0, "")
        except PermissionError:
            return (f"错误: 没有权限读取文件: {wildcard_file}", 0, "")
        except Exception as e:
            error_msg = f"错误: 读取文件失败: {str(e)}"
            print(error_msg)
            return (error_msg, 0, "")


class 数值分割节点:
    """数值分割节点 - 将空格分隔的数值字符串分割为6个独立输出"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "数值字符串": ("STRING", {
                    "default": "1 2 3 5 9",
                    "multiline": False,
                    "placeholder": "输入用空格分隔的数值，如: 1 2 3 5 9",
                    "tooltip": "输入用空格分隔的数值字符串，将被分割为6个独立输出端口。支持整数和浮点数，例如：1 2.5 3 4.7 5"
                }),
            }
        }
    
    # 定义输出类型和名称
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("数值1", "数值2", "数值3", "数值4", "数值5","数值6")
    
    # 处理函数名称
    FUNCTION = "分割数值"
    
    # 节点分类
    CATEGORY = "🐱 CATS"
    
    def 分割数值(self, 数值字符串):
        """
        将空格分隔的数值字符串分割为6个字符串输出
        
        参数:
            数值字符串: 用空格分隔的数值字符串
            
        返回:
            tuple: 包含6个字符串的元组，对应6个输出端口
        """
        try:
            # 分割字符串并保留原始格式
            数值列表 = 数值字符串.strip().split()
            
            # 确保有5个数值，如果不足则用"0"填充，多余则截断
            while len(数值列表) < 6:
                数值列表.append("0")
            if len(数值列表) > 6:
                数值列表 = 数值列表[:6]
            
            # 直接返回字符串元组
            return tuple(数值列表)
        except Exception as e:
            # 如果解析失败，返回默认字符串值
            return ("0", "0", "0", "0", "0", "0")


class ReversePromptSaveNode:
    """图片反推提示词保存节点
    
    用于保存图片反推的提示词到txt文档，支持单张和批量保存模式。
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "placeholder": "在此输入反推的提示词..."}),
                "save_path": ("STRING", {"default": "E:/Project1/Wildcards-Generator/prompts", "vfile": {".": {"accept": ".", "save": True}}}),
                "file_name": ("STRING", {"default": "reverse_prompt.txt"}),
                "save_mode": (["single_file", "batch_mode"], {"default": "single_file"}),
            },
            "optional": {
                "image_name": ("STRING", {"default": "", "placeholder": "输入图片名称（批量模式使用）"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "save_reverse_prompt"
    OUTPUT_NODE = True
    CATEGORY = "🐱 CATS"
    
    def save_reverse_prompt(self, prompt, save_path, file_name, save_mode, image_name=""):
        """保存反推提示词到文件
        
        参数:
        - prompt: 反推的提示词
        - save_path: 保存路径
        - file_name: 文件名
        - save_mode: 保存模式，single_file或batch_mode
        - image_name: 图片名称（批量模式使用）
        
        返回:
        - prompt: 返回输入提示词，保持数据流
        """
        try:
            # 确保提示词不为空
            if not prompt or not prompt.strip():
                return {
                    "ui": {
                        "text": [
                            "错误: 提示词为空",
                            "请输入有效的提示词或连接反推节点"
                        ]
                    },
                    "result": (prompt,)
                }
            
            # 确保保存路径存在
            Path(save_path).mkdir(parents=True, exist_ok=True)
            
            # 构建基础文件名（不含扩展名）
            base_name, _ = os.path.splitext(file_name)  # 忽略输入的扩展名
            ext = ".txt"  # 强制使用.txt扩展名
            
            file_path = ""
            
            if save_mode == "single_file":
                # 单文件模式：每次执行保存为新文件，自动添加累计数字
                counter = 0
                while True:
                    if counter == 0:
                        temp_file_path = os.path.join(save_path, f"{base_name}{ext}")
                    else:
                        temp_file_path = os.path.join(save_path, f"{base_name}{counter}{ext}")
                    
                    if not os.path.exists(temp_file_path):
                        file_path = temp_file_path
                        break
                    counter += 1
                
                # 保存文件
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(prompt.strip() + "\n")
                
                message = f"提示词已保存到新文件"
                saved = True
            else:
                # batch_mode模式：
                if image_name:
                    # 如果提供了图片名称，为每张图片创建单独的txt文件
                    image_base_name, _ = os.path.splitext(image_name)
                    file_path = os.path.join(save_path, f"{image_base_name}{ext}")
                    
                    # 保存文件
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(prompt.strip() + "\n")
                    
                    message = f"提示词已保存到图片专属文件"
                    saved = True
                else:
                    # 没有提供图片名称，汇总到同一文件
                    file_path = os.path.join(save_path, f"{base_name}{ext}")
                    
                    # 追加到文件
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(prompt.strip() + "\n")
                    
                    message = f"提示词已添加到汇总文件"
                    saved = True
            
            # 准备UI输出
            ui_output = {
                "text": [
                    prompt.strip(),
                    "",
                    message,
                    f"文件: {file_path}",
                    f"大小: {os.path.getsize(file_path)} 字节"
                ]
            }
            
            return {
                "ui": ui_output,
                "result": (prompt,)
            }
        except Exception as e:
            error_msg = f"操作失败: {str(e)}"
            return {
                "ui": {
                    "text": [
                        error_msg,
                        f"错误: {type(e).__name__}"
                    ]
                },
                "result": (prompt,)
            }


# 全局模型缓存
MODEL_CACHE = {}

class aistudynow_QwenVL:
    """Qwen3-VL 图像/视频理解节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image": ("IMAGE", {"shape": [7]}),
                "video": ("IMAGE", {"shape": [7]}),
                "custom_prompt": ("STRING", {"forceInput": True}),
            },
            "widget": {
                "model": (["Qwen3-VL-2B-Instruct", "Qwen3-VL-4B-Instruct", 
                          "Qwen3-VL-8B-Instruct", "Qwen3-VL-32B-Instruct",
                          "Qwen2.5-VL-3B-Instruct", "Qwen2.5-VL-7B-Instruct",
                          "Qwen2.5-VL-72B-Instruct"], 
                         {"default": "Qwen3-VL-2B-Instruct"}),
                "quantization": (["none", "4-bit (VRAM-friendly)", 
                                 "8-bit", "FP16"], 
                                {"default": "4-bit (VRAM-friendly)"}),
                "system_prompt": ("STRING", {"multiline": True, 
                                    "default": "Describe this image in detail."}),
                "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 8192}),
                "use_image_resolution": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, 
                         "max": 0xffffffffffffffff}),
                "seed_mode": (["fixed", "randomize", "increment"], 
                             {"default": "fixed"}),
                "device": (["auto", "cuda", "cpu", "mps"], 
                          {"default": "auto"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "analyze"
    CATEGORY = "🐱 CATS"
    
    def load_model(self, model_name, quantization, device):
        """加载Qwen3-VL模型"""
        try:
            # 生成缓存键
            cache_key = f"{model_name}_{quantization}_{device}"
            
            # 检查缓存
            if cache_key in MODEL_CACHE:
                return MODEL_CACHE[cache_key]
            
            # 尝试导入依赖
            from transformers import AutoModelForVision2Seq, AutoProcessor
            from transformers import BitsAndBytesConfig
            import torch
            
            # 配置量化
            quantization_config = None
            if quantization == "4-bit (VRAM-friendly)":
                quantization_config = BitsAndBytesConfig(load_in_4bit=True)
            elif quantization == "8-bit":
                quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            
            # 加载模型
            model = AutoModelForVision2Seq.from_pretrained(
                f"Qwen/{model_name}",
                quantization_config=quantization_config,
                torch_dtype=torch.float16 if quantization == "FP16" else None,
                device_map=device
            )
            
            # 加载处理器
            processor = AutoProcessor.from_pretrained(f"Qwen/{model_name}")
            
            # 缓存模型
            MODEL_CACHE[cache_key] = (model, processor)
            
            return model, processor
        except Exception as e:
            raise Exception(f"模型加载失败: {str(e)}")
    
    def preprocess_image(self, image_tensor, use_original_resolution):
        """预处理图像"""
        import torch
        from PIL import Image
        import numpy as np
        
        # 确保输入是张量
        if not isinstance(image_tensor, torch.Tensor):
            image_tensor = torch.tensor(image_tensor)
        
        # 处理batch维度
        if len(image_tensor.shape) == 4:
            # [B, H, W, C]
            images = []
            for i in range(image_tensor.shape[0]):
                img = image_tensor[i].cpu().numpy()
                # 转换值域从[0,1]到[0,255]
                img = (img * 255).astype(np.uint8)
                pil_img = Image.fromarray(img)
                
                # 调整分辨率
                if not use_original_resolution:
                    max_size = 1024
                    w, h = pil_img.size
                    if w > h:
                        new_w = max_size
                        new_h = int(h * (max_size / w))
                    else:
                        new_h = max_size
                        new_w = int(w * (max_size / h))
                    pil_img = pil_img.resize((new_w, new_h))
                
                images.append(pil_img)
            return images
        else:
            # 单张图像 [H, W, C]
            img = image_tensor.cpu().numpy()
            img = (img * 255).astype(np.uint8)
            pil_img = Image.fromarray(img)
            
            if not use_original_resolution:
                max_size = 1024
                w, h = pil_img.size
                if w > h:
                    new_w = max_size
                    new_h = int(h * (max_size / w))
                else:
                    new_h = max_size
                    new_w = int(w * (max_size / h))
                pil_img = pil_img.resize((new_w, new_h))
            
            return [pil_img]
    
    def preprocess_video(self, video_tensor, max_frames=8):
        """预处理视频帧"""
        import torch
        from PIL import Image
        import numpy as np
        
        # 确保输入是张量
        if not isinstance(video_tensor, torch.Tensor):
            video_tensor = torch.tensor(video_tensor)
        
        # [Frames, H, W, C]
        frames = []
        total_frames = video_tensor.shape[0]
        
        # 均匀采样最多max_frames帧
        if total_frames <= max_frames:
            sample_indices = range(total_frames)
        else:
            sample_indices = np.linspace(0, total_frames - 1, max_frames, dtype=int)
        
        for i in sample_indices:
            img = video_tensor[i].cpu().numpy()
            img = (img * 255).astype(np.uint8)
            pil_img = Image.fromarray(img)
            frames.append(pil_img)
        
        return frames
    
    def analyze(self, image=None, video=None, custom_prompt="", 
                model="Qwen3-VL-2B-Instruct", quantization="4-bit (VRAM-friendly)",
                system_prompt="Describe this image in detail.", 
                max_tokens=1024, use_image_resolution=True, 
                seed=0, seed_mode="fixed", device="auto"):
        """分析图像/视频并生成描述"""
        try:
            # 处理种子
            import random
            import torch
            
            if seed_mode == "randomize":
                seed = random.randint(0, 0xffffffffffffffff)
            elif seed_mode == "increment":
                # 简单实现，实际应该使用持久化存储
                seed += 1
            
            # 设置随机种子
            torch.manual_seed(seed)
            random.seed(seed)
            
            # 确定设备
            if device == "auto":
                device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # 检查输入
            if image is None and video is None:
                return ("错误: 请提供图像或视频输入",)
            
            # 加载模型
            model, processor = self.load_model(model, quantization, device)
            
            # 处理输入
            if image is not None:
                images = self.preprocess_image(image, use_image_resolution)
            else:
                images = self.preprocess_video(video)
            
            # 构建对话消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": []}
            ]
            
            # 添加图像
            for img in images:
                messages[1]["content"].append({"type": "image", "image": img})
            
            # 添加文本提示
            if custom_prompt:
                messages[1]["content"].append({"type": "text", "text": custom_prompt})
            else:
                messages[1]["content"].append({"type": "text", "text": "Describe this image."})
            
            # 生成输入
            input_text = processor.apply_chat_template(messages, tokenize=False)
            inputs = processor(
                text=input_text,
                images=images[0] if images else None,
                return_tensors="pt"
            ).to(device)
            
            # 模型推理
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=0.7
                )
            
            # 解码输出
            response = processor.batch_decode(outputs, skip_special_tokens=True)[0]
            
            # 提取assistant回复
            if "assistant" in response:
                response = response.split("assistant")[-1].strip()
            
            return (response,)
        except Exception as e:
            error_msg = f"分析失败: {str(e)}"
            print(error_msg)
            return (error_msg,)


def pil_to_tensor(image):
    img_np = np.array(image).astype(np.float32) / 255.0
    return torch.from_numpy(img_np).unsqueeze(0)

class ImageSequenceLoader:
    # --- 节点状态持久化 ---
    image_list = []
    current_index = -1
    # 存储标准化的路径，确保比较的稳定性
    _last_folder_path_standardized = "" 
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "input/sequence_folder", "multiline": False}),
                "trigger": ("INT", {"default": 0, "hidden": True}), 
            },
            "optional": {
                "filename_display": ("STRING", {"forceInput": True, "widget": "text", "default": "Waiting...", "hidden": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE_OUT", "FILENAME")
    FUNCTION = "execute"
    CATEGORY = "🐱 CATS"
    
    def execute(self, folder_path, trigger, filename_display=None):
        
        # 🚨 修正点 1: 路径标准化
        # 获取绝对路径，并将 Windows 反斜杠 (\) 转换为稳定的正斜杠 (/)
        try:
            standardized_path = os.path.abspath(folder_path).replace("\\", "/")
        except Exception:
            standardized_path = folder_path.replace("\\", "/")
        
        # 1. 检查路径变化 / 初始化
        # 只有当标准化路径与上次存储的路径不一致时，才重新加载文件列表
        if standardized_path != self._last_folder_path_standardized:
            self._last_folder_path_standardized = standardized_path # 更新存储的路径
            
            valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
            
            try:
                # 使用标准化的路径进行文件操作
                all_files = os.listdir(standardized_path)
                image_files_with_path = []

                for f in all_files:
                    full_path = os.path.join(standardized_path, f)
                    if os.path.isfile(full_path) and f.lower().endswith(tuple(valid_extensions)):
                        # 按修改时间排序
                        image_files_with_path.append((f, os.path.getmtime(full_path))) 

                # 按修改时间排序
                image_files_with_path.sort(key=lambda x: x[1])
                self.image_list = [f[0] for f in image_files_with_path]

                print(f"ImageSequenceLoader: Loaded {len(self.image_list)} images from: {standardized_path}. Sorted by modification time.")

            except FileNotFoundError:
                 raise Exception(f"ImageSequenceLoader Error: Folder not found or inaccessible: {standardized_path}")

            # 🚨 修正点 2: 只有在路径发生变化时重置为 -1
            self.current_index = -1 
        
        # 2. 检查列表是否为空
        if not self.image_list:
            raise Exception("ImageSequenceLoader Error: Folder is empty or contains no valid images.")

        # 3. 自动切换到下一张图片（每次执行都 +1）
        # 如果路径稳定，current_index 将递增；如果路径变化，current_index 从 -1 变为 0。
        self.current_index = (self.current_index + 1) % len(self.image_list)
        
        # 4. 加载图片
        filename = self.image_list[self.current_index]
        full_path = os.path.join(standardized_path, filename) # 使用标准化路径加载

        try:
            image = Image.open(full_path).convert("RGB")
            image_tensor = pil_to_tensor(image)
        except Exception as e:
            print(f"ImageSequenceLoader Error: loading image {full_path}: {e}")
            raise

        # 5. 返回结果
        return (image_tensor, filename)
