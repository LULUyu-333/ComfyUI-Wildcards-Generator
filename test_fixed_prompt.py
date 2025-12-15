# 测试固定提示词功能

import os
import sys
import tempfile

# 添加插件目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'wildcards_generator'))

from wildcards_generator.nodes import RandomWildcardNode

print("=== 固定提示词功能测试 ===")

# 创建临时wildcards文件
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
    f.write("提示词1\n")
    f.write("提示词2\n")
    f.write("提示词3\n")
    wildcards_file = f.name

try:
    node = RandomWildcardNode()
    
    print("\n1. 测试无固定提示词情况")
    result = node.get_random_prompt(
        wildcard_file=wildcards_file,
        num_prompts=1,
        seed=1234,
        fixed_prompt=""
    )
    print(f"结果: {result[0]}")
    
    print("\n2. 测试单个随机提示词+固定提示词")
    result = node.get_random_prompt(
        wildcard_file=wildcards_file,
        num_prompts=1,
        seed=1234,
        fixed_prompt="黑色头发"
    )
    print(f"固定提示词: 黑色头发")
    print(f"结果: {result[0]}")
    assert "黑色头发" in result[0], "固定提示词未正确添加"
    
    print("\n3. 测试多个随机提示词+固定提示词")
    result = node.get_random_prompt(
        wildcard_file=wildcards_file,
        num_prompts=3,
        seed=1234,
        fixed_prompt="黑色头发"
    )
    print(f"固定提示词: 黑色头发")
    print(f"结果:")
    for i, line in enumerate(result[0].split('\n'), 1):
        print(f"  {i}. {line}")
        assert "黑色头发" in line, f"第{i}行固定提示词未正确添加"
    
    print("\n4. 测试不同的固定提示词")
    result = node.get_random_prompt(
        wildcard_file=wildcards_file,
        num_prompts=2,
        seed=1234,
        fixed_prompt="蓝色眼睛"
    )
    print(f"固定提示词: 蓝色眼睛")
    print(f"结果:")
    for i, line in enumerate(result[0].split('\n'), 1):
        print(f"  {i}. {line}")
        assert "蓝色眼睛" in line, f"第{i}行固定提示词未正确添加"
    
    print("\n5. 测试复杂固定提示词")
    result = node.get_random_prompt(
        wildcard_file=wildcards_file,
        num_prompts=2,
        seed=1234,
        fixed_prompt="美丽的女孩，穿着红色连衣裙"
    )
    print(f"固定提示词: 美丽的女孩，穿着红色连衣裙")
    print(f"结果:")
    for i, line in enumerate(result[0].split('\n'), 1):
        print(f"  {i}. {line}")
    
    print("\n=== 所有测试通过! 固定提示词功能正常工作 ===")
    
except Exception as e:
    print(f"\n=== 测试失败: {e} ===")
    import traceback
    traceback.print_exc()
finally:
    # 清理临时文件
    os.unlink(wildcards_file)
