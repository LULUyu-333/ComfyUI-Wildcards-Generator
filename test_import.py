# 测试插件导入功能

try:
    # 尝试导入插件
    import sys
    import os
    
    # 添加插件目录到Python路径
    plugin_dir = os.path.join(os.path.dirname(__file__), 'wildcards_generator')
    sys.path.append(plugin_dir)
    
    print("=== 测试插件导入 ===")
    print(f"插件目录: {plugin_dir}")
    print(f"是否存在: {os.path.exists(plugin_dir)}")
    
    # 尝试导入节点
    from wildcards_generator import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    
    print("\n=== 节点映射 ===")
    print(f"NODE_CLASS_MAPPINGS: {NODE_CLASS_MAPPINGS}")
    print(f"NODE_DISPLAY_NAME_MAPPINGS: {NODE_DISPLAY_NAME_MAPPINGS}")
    
    # 尝试实例化节点
    print("\n=== 节点实例化测试 ===")
    for node_name, node_class in NODE_CLASS_MAPPINGS.items():
        print(f"\n测试节点: {node_name}")
        print(f"节点类: {node_class}")
        
        # 检查节点的INPUT_TYPES
        input_types = node_class.INPUT_TYPES()
        print(f"INPUT_TYPES: {input_types}")
        
        # 检查节点的其他属性
        print(f"RETURN_TYPES: {node_class.RETURN_TYPES}")
        print(f"FUNCTION: {node_class.FUNCTION}")
        print(f"OUTPUT_NODE: {getattr(node_class, 'OUTPUT_NODE', False)}")
        print(f"CATEGORY: {node_class.CATEGORY}")
    
    print("\n=== 测试通过! 插件可以正常导入和使用 ===")
    
except Exception as e:
    print(f"\n=== 测试失败: {e} ===")
    import traceback
    traceback.print_exc()
