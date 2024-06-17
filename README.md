# README

## 快速开始

**功能：将 ChatGPT 的回答复制到 Markdown 文件并正常编译数学公式**

1. 使用 ChatGPT 左下角的复制按钮复制回答内容。
2. 手动粘贴到某个 Markdown 文件中。此时由于一些符号问题，数学公式可能不能正常显示。目前，Obsidian 和 Typora 确实有这种问题。
3. 使用 `gpt2md_math.exe (\dist文件夹中)` 选择 Markdown 文件，程序将自动执行修改。在 Markdown 编辑器中刷新即可。
4. 或者直接粘贴文本，按照用户界面提示操作。

视频演示：[【数学科研向】将 ChatGPT 的回答复制到 Markdown 文件并正常编译数学公式_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1HCV7eyEjm/?vd_source=5d46585e70bbcd5b429ae7cdb6f1e701)



## 用户使用说明

#### 工具概述
本工具是一款用于文本替换的应用程序，能够根据特定规则对文本进行修改，并将修改后的文本自动复制到剪切板。工具还支持直接选择并修改Markdown文件。

#### 界面说明
- **左侧文本窗口**：标题为“将ChatGPT复制的内容粘贴到这里”。在此窗口中粘贴需要修改的原始文本。
- **右侧文本窗口**：标题为“修改后的内容（已默认复制在剪切板）”。此窗口将显示根据特定规则修改后的文本，并且修改后的内容会自动复制到剪切板。
- **选择并替换MD文件按钮**：点击此按钮可以选择一个Markdown文件，程序将对该文件执行文本替换操作并保存修改。

#### 使用步骤
1. 打开应用程序。
2. 在左侧文本窗口中粘贴需要修改的原始文本。
3. 右侧文本窗口将自动显示修改后的文本，且修改后的内容会自动复制到剪切板。
4. 如果需要直接修改Markdown文件，点击“选择并替换MD文件”按钮，选择需要修改的Markdown文件，程序将自动进行文本替换并保存。



## 开发者说明

#### 环境要求
- Python 3.x
- 必需的Python库：
  - `tkinter`：用于创建图形用户界面。
  - `re`：用于执行正则表达式操作。
  - `pyperclip`：用于复制文本到剪切板。

#### 安装依赖
使用以下命令安装所需的Python库：
```bash
pip install pyperclip
```

#### 源代码结构
```python
import tkinter as tk
from tkinter import filedialog
import re
import pyperclip

def replace_text(content):
    # 文本替换函数，执行特定的文本替换操作
    replacements = {
        r'\\\[': '$$',
        r'\\\]': '$$',
        r'\\\)': '$',
        r'\\\(': '$',
    }
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

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
root.title("文本替换工具")

# 创建选择文件并替换按钮
replace_button = tk.Button(root, text="选择并替换MD文件", command=open_and_replace_file)
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

def on_input_text_change(event):
    input_text_widget.edit_modified(False)
    update_output_text()

input_text_widget.bind("<<Modified>>", on_input_text_change)

# 启动主循环
root.mainloop()
```

#### 打包为可执行文件
使用 PyInstaller 将 Python 脚本转换为可执行文件：
```bash
pyinstaller --onefile --noconsole --name gpt2md_math your_script.py
```

生成的可执行文件将在 `dist` 文件夹中，名为 `gpt2md_math.exe`。

#### 功能说明
- **replace_text(content)**：对输入文本执行一系列替换操作。
- **update_output_text(event=None)**：更新右侧文本窗口的内容并复制到剪切板。
- **select_file()**：打开文件选择对话框，供用户选择一个Markdown文件。
- **replace_text_in_file(file_path)**：对选择的Markdown文件执行文本替换操作。
- **open_and_replace_file()**：选择并替换Markdown文件的操作流程。

#### 事件绑定
- **on_input_text_change(event)**：确保每次左侧文本窗口内容修改时触发更新。

#### 用户界面设计
使用 `tkinter` 创建主窗口、按钮、文本框和标签，实现文本替换工具的用户界面。
