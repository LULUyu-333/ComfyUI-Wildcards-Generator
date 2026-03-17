# 文件路径: custom_nodes/ComfyUI_ImageSequenceLoader/image_sequence_node.py

import os
import torch
from PIL import Image
import numpy as np

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
    CATEGORY = "文件/序列"
    
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
