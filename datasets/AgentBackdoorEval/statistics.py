import json
import os

# 定义数据集文件夹名称和结果文件名称
split = ['Banking-Finance', 'E-commerce', 'Medical', 'Social-Media', 'Weather-Query']
result_files = {
    'Banking-Finance': ['review_base64_result.json', 'review_Original_result.json', 'review_results_test.json'],
    'E-commerce': ['review_base64_result.json', 'review_Original_result.json', 'review_results_test.json'],
    'Medical': ['review_base64_result.json', 'review_Original_result.json', 'review_results_test.json'],
    'Social-Media': ['review_base64_result.json', 'review_Original_result.json', 'review_results_test.json'],
    'Weather-Query': ['review_base64_result.json', 'review_Original_result.json', 'review_results_test.json']
}

# 定义一个函数来计算检出率
def calculate_detection_rate(result_files):
    for domain, files in result_files.items():
        for file in files:
            file_path = f'Decomposed_data/result/{domain}/{file}'  # 构建文件路径
            if os.path.exists(file_path):
                # 读取JSON文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 计算检出率
                total = len(data)
                detected = sum(1 for entry in data if entry['review_result'] is False)
                detection_rate = detected / total * 100 if total > 0 else 0

                # 输出检出率
                print(f"{domain} - {file}: Detection Rate (DR) = {detection_rate:.2f}%")

                # 保存结果到一个新文件，记录该领域的检出率
                result = {
                    'domain': domain,
                    'file': file,
                    'detection_rate': detection_rate
                }

                # 将检出率写入到结果文件夹中
                result_output_path = f'Decomposed_data/result/{domain}/detection_rate_results.json'
                with open(result_output_path, 'a', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                    f.write("\n")
            else:
                print(f"File {file_path} does not exist.")

# 调用函数计算检出率
calculate_detection_rate(result_files)
