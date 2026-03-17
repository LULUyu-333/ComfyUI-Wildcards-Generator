from .folder_image_loader import ImageBatchLoaderNode

NODE_CLASS_MAPPINGS = {
    "ImageBatchLoaderNode": ImageBatchLoaderNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBatchLoaderNode": "图像批量加载节点",
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
