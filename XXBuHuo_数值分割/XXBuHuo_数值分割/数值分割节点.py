# 数值分割节点 - 支持5个数值输出端口
# 作者: AI Assistant
# 版本: 1.0
# 功能: 将输入的空格分隔数值字符串分割为6个独立输出

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
    CATEGORY = "工具节点"
    
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

# 节点注册
def 注册节点():
    return {
        "数值分割节点": 数值分割节点
    }

# 导出节点映射
NODE_CLASS_MAPPINGS = {
    "数值分割节点": 数值分割节点
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "数值分割节点": "数值分割节点"
}