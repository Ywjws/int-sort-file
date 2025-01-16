import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def find_and_rename_files(root_dir):
    pattern = re.compile(r'^(.*?)(\s*\(\d+\))\.png$')  # 匹配格式为 xxxx (数字).png 的文件名
    renamed_files = []  # 用于记录重命名的文件信息

    for file in os.listdir(root_dir):  # 遍历指定目录中的所有文件
        match = pattern.match(file)  # 匹配文件名
        if match:
            prefix = match.group(1).strip()  # 获取xxxx部分，去掉多余空格
            number = re.findall(r'\d+', match.group(2))[0]  # 提取数字部分
            new_number = f'{int(number):07d}'  # 将数字转为7位数，前面补零
            new_file_name = f'{prefix} ({new_number}).png'  # 新的文件名
            old_file_path = os.path.join(root_dir, file)  # 旧文件的完整路径
            new_file_path = os.path.join(root_dir, new_file_name)  # 新文件的完整路径
            
            os.rename(old_file_path, new_file_path)  # 重命名文件
            renamed_files.append(f'Renamed: {old_file_path} -> {new_file_path}')  # 记录重命名信息

    return renamed_files

def select_directory():
    dir_path = filedialog.askdirectory()  # 打开文件夹选择对话框
    if dir_path:
        root_dir.set(dir_path)  # 设置选择的目录

def start_renaming():
    directory = root_dir.get()  # 获取输入的目录
    if not directory:
        messagebox.showwarning("警告", "请先选择一个目录。")  # 如果没有选择目录，显示警告
        return
    renamed_files = find_and_rename_files(directory)  # 执行重命名操作
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)  # 清空日志框
    for message in renamed_files:
        log_text.insert(tk.END, message + '\n')  # 将重命名信息插入日志框
    log_text.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("文件重命名工具")

# 创建输入框和按钮
root_dir = tk.StringVar()
tk.Label(root, text="选择根目录:").pack(pady=5)
tk.Entry(root, textvariable=root_dir, width=50).pack(pady=5)
tk.Button(root, text="浏览", command=select_directory).pack(pady=5)
tk.Button(root, text="开始重命名", command=start_renaming).pack(pady=10)

# 创建日志框
log_text = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
log_text.pack(pady=5)

# 运行主循环
root.mainloop()
