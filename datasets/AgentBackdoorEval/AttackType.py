import re

# 读取 backdoor_stats.txt 文件
def count_unique_attacks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 使用正则表达式提取事件名
    pattern = r"(\w+) triggered at"
    attacks = set()  # 使用集合存储事件名，集合自动去重

    for line in lines:
        match = re.search(pattern, line)
        if match:
            event_name = match.group(1)  # 获取事件名
            attacks.add(event_name)  # 将事件名添加到集合中，集合会自动去重

    # 输出结果
    return len(attacks), attacks

# 文件路径
file_path = 'Encryption_data/result/Banking-Finance/backdoor_stats.txt'

# 获取唯一的攻击数量和攻击事件名
unique_attack_count, attack_names = count_unique_attacks(file_path)

# 打印统计结果
print(f"Total unique attacks: {unique_attack_count}")
for attack in attack_names:
    print(attack)
