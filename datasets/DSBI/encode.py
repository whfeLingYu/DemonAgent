import base64
import json
split = ['Banking-Finance','E-commerce','Medical','Social-Media','Weather-Query']
# 定义一个函数来替换时间戳和工具调用
ifbase64 = True
def replace_time_with_tool(result_file, backdoor_dict):
    updated_result_file = []

    for entry in result_file:
        updated_memory = entry["memory"]
        lines = updated_memory.split("\n")

        for i, line in enumerate(lines):
            if "Human:" in line and "time" in line:
                # 检查下行是否是AI时间戳，并确保不会超出范围
                if i + 1 < len(lines) and "AI: " in lines[i + 1] and "_" in lines[i + 1]:
                    timestamp = lines[i + 1].split("AI: ")[1].strip()  # 获取时间戳

                    # 查找接下来的Action行，不再要求是固定的i+3，而是扫描后续行
                    for j in range(i + 2, len(lines)):
                        if "Action: " in lines[j]:
                            tool_line = lines[j]
                            # 提取工具名
                            tool = tool_line.split("Action: ")[1].strip()

                            # 如果工具存在于backdoor字典中，替换时间戳行
                            if tool in backdoor_dict:
                                backdoor_code = backdoor_dict[tool]
                                if ifbase64:
                                    # 对backdoor代码进行base64编码
                                    base64_backdoor_code = base64.b64encode(backdoor_code.encode()).decode()
                                    print(f"Base64 encoded backdoor code: {base64_backdoor_code}")
                                    lines[i + 1] = f"{base64_backdoor_code}"  # 替换时间戳行
                                else:
                                    lines[i + 1] = f"{backdoor_code}"  # 直接替换为backdoor代码
                                break  # 找到第一个Action后就停止进一步扫描

        # 更新记忆内容
        updated_entry = entry.copy()
        updated_entry["memory"] = "\n".join(lines)
        updated_result_file.append(updated_entry)

    return updated_result_file

# 批量处理所有分类文件
for category in split:
    dataset_path = f'Decomposed_data/{category}.json'
    result_path = f'Decomposed_data/result/{category}/result.json'
    output_path = f'Decomposed_data/result/{category}/base64_result.json'

    # 读取dataset文件和result_file文件
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    with open(result_path, 'r', encoding='utf-8') as f:
        result_file = json.load(f)

    # 构建backdoor behavior字典
    backdoor_dict = {}
    for entry in dataset:
        for tool, behavior in entry["backdoor behavior"].items():
            backdoor_dict[tool] = behavior

    # 调用函数处理结果文件
    updated_result_file = replace_time_with_tool(result_file, backdoor_dict)

    # 保存处理后的结果到一个新的文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(updated_result_file, f, ensure_ascii=False, indent=4)

    print(f"Updated result file for {category} has been saved as '{output_path}'.")
