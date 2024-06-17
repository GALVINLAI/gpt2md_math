import tkinter as tk
from tkinter import filedialog
import re
import pyperclip


"""
使用 PyInstaller 将 Python 脚本转换为可执行文件：
pyinstaller --onefile --noconsole --name gpt2md_math your_script.py
"""


def replace_text(content):
    """
    这个函数的功能是对文本内容进行以下几种文本替换操作：
    1. 将所有 \[ 替换为 $$。
    2. 将所有 \] 替换为 $$。
    3. 将所有 \) 替换为 $。
    4. 将所有 \( 替换为 $。
    5. 找到被单个 $ 包围的文本，去掉该文本第一个空格（如果该文本第一位是空格的话）。
    6. 找到被单个 $ 包围的文本，去掉该文本最后一个空格（如果该文本最后一位是空格的话）。
    """
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
    return content

def update_output_text(event=None):
    input_text = input_text_widget.get("1.0", tk.END)
    modified_text = replace_text(input_text)
    output_text_widget.delete("1.0", tk.END)
    output_text_widget.insert(tk.END, modified_text)
    pyperclip.copy(modified_text)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
    return file_path

def replace_text_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified_content = replace_text(content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    print(f"Text replaced in {file_path}")

def open_and_replace_file():
    file_path = select_file()
    if file_path:
        replace_text_in_file(file_path)
    else:
        print("No file selected")

# 创建主窗口
root = tk.Tk()
root.title("gpt2md_math (https://github.com/GALVINLAI/gpt2md_math)")

# 创建选择文件并替换按钮
replace_button = tk.Button(root, text="手动选择并替换md文件", command=open_and_replace_file)
replace_button.pack(pady=10)

# 创建左侧文本框和标签
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
left_label = tk.Label(left_frame, text="将ChatGPT复制的内容粘贴到这里")
left_label.pack()
input_text_widget = tk.Text(left_frame, wrap="word", width=50, height=20)
input_text_widget.pack(fill=tk.BOTH, expand=True)
input_text_widget.bind("<<Modified>>", update_output_text)

# 创建右侧文本框和标签
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
right_label = tk.Label(right_frame, text="修改后的内容（已默认复制在剪切板）")
right_label.pack()
output_text_widget = tk.Text(right_frame, wrap="word", width=50, height=20)
output_text_widget.pack(fill=tk.BOTH, expand=True)

# 确保每次内容修改时触发更新
def on_input_text_change(event):
    input_text_widget.edit_modified(False)
    update_output_text()

input_text_widget.bind("<<Modified>>", on_input_text_change)

# 启动主循环
root.mainloop()
