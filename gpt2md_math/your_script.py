import tkinter as tk
from tkinter import filedialog
import re

"""
作者：ChatGPT
日期：2024年6月16日

使用方法：
1. 将本脚本保存为 your_script.py 文件。

2. 使用 PyInstaller 将 Python 脚本转换为可执行文件：
   $ pyinstaller --onefile --noconsole --name gpt2md_math your_script.py

3. 运行 gpt2md_math.exe (\dist 文件夹)，选择需要处理的 Markdown 文件，程序将自动进行指定的文本替换操作并保存。
"""

def select_file():
    """
    打开文件选择对话框，供用户选择一个 Markdown 文件。
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
    return file_path

def replace_text_in_file(file_path):
    """
    这个函数的功能是对指定的 Markdown 文件进行以下几种文本替换操作：
    1. 将所有 \[ 替换为 $$。
    2. 将所有 \] 替换为 $$。
    3. 将所有 \) 替换为 $。
    4. 将所有 \( 替换为 $。
    5. 找到被单个 $ 包围的文本，去掉该文本第一个空格（如果该文本第一位是空格的话）。
    6. 找到被单个 $ 包围的文本，去掉该文本最后一个空格（如果该文本最后一位是空格的话）。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 执行替换操作
    replacements = {
        r'\\\[': '$$',
        r'\\\]': '$$',
        r'\\\)': '$',
        r'\\\(': '$',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    # 替换被单个 $ 包围的文本，去掉第一个和最后一个空格
    def replace_spaces(match):
        text = match.group(1)
        if text.startswith(' '):
            text = text[1:]
        if text.endswith(' '):
            text = text[:-1]
        return f'${text}$'
    
    content = re.sub(r'\$([^\$]*?)\$', replace_spaces, content)

    # 将替换后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Text replaced in {file_path}")

def main():
    """
    主函数，选择文件并进行文本替换。
    """
    file_path = select_file()
    if file_path:
        replace_text_in_file(file_path)
    else:
        print("No file selected")

if __name__ == "__main__":
    main()

# 文件修改时间：2024年6月16日
