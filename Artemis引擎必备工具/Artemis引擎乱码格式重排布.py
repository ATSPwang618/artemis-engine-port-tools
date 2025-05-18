import os
import re

# 定义替换规则
replacements = [
    (r'ast = \{block_00000', r'ast = {\n\tblock_00000'),
    (r'block_00000 = \{\{"savetitle", text=', r'block_00000 = {\n\t\t{"savetitle", text='),
    (r',(block_\w+)', r',\n\t\1'),
    (r'\},\{', r'},\n\t\t{'),
    (r',text', r',\n\t\ttext'),
    (r'text = \{', r'text = {\n\t\t'),
    (r',linkback', r',\n\t\tlinkback'),
    (r'\{\{"text"\},', r'{\n\t\t{"text"},'),
    (r'vo = {', r'\tvo = {'),
    (r'ja =', r'\n\t\t\tja ='),
    (r'= \{\{"fg",', r'= {\n\t\t{"fg",'),
    (r'= \{\{"msgoff"', r'= {\n\t\t{"msgoff"')
]

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ast'):
                file_path = os.path.join(root, file)
                process_file(file_path)
                print(f"Processed {file_path}")

# 使用原始字符串表示文件夹路径
folder_path = r'C:\Users\Administrator\Desktop\test\test1'
process_folder(folder_path)
