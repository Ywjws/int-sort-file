import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def copy_and_rename_files(src_directory, dest_directory):
    try:
        # 获取源目录中的所有文件
        files = os.listdir(src_directory)

        # 筛选出所有文件（忽略扩展名）
        files = [f for f in files if os.path.isfile(os.path.join(src_directory, f))]

        # 使用正则表达式提取文件名中的数字部分
        file_name_pattern = re.compile(r'(\d+)')

        # 排序文件：按文件名中的数字部分进行排序
        sorted_files = sorted(files, key=lambda f: int(file_name_pattern.findall(f)[0]) if file_name_pattern.findall(f) else 0)

        # 确保目标文件夹存在
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        # 复制并重命名文件
        for i, file in enumerate(sorted_files, 1):
            # 提取文件名和扩展名
            file_name, file_extension = os.path.splitext(file)

            # 新的文件名，按照顺序编号
            new_file_name = f"{i}{file_extension}"

            # 获取源文件路径和目标文件路径
            src_file_path = os.path.join(src_directory, file)
            dest_file_path = os.path.join(dest_directory, new_file_name)

            # 复制文件到目标目录并重命名
            shutil.copy(src_file_path, dest_file_path)
        
        messagebox.showinfo("成功", "文件复制并重命名完成！")

    except Exception as e:
        messagebox.showerror("错误", f"发生错误: {str(e)}")

def select_directory(label):
    # 打开文件夹选择对话框
    directory = filedialog.askdirectory()
    if directory:
        label.config(text=directory)

def start_copying():
    src_directory = src_label.cget("text")
    dest_directory = dest_label.cget("text")

    if not src_directory or not dest_directory:
        messagebox.showwarning("警告", "请确保选择了源目录和目标目录！")
    else:
        copy_and_rename_files(src_directory, dest_directory)

# 创建主窗口
root = tk.Tk()
root.title("文件复制并重命名工具")
root.geometry("400x200")

# 源目录选择部分
src_label = tk.Label(root, text="选择源目录", width=50, anchor='w')
src_label.pack(pady=10)

src_button = tk.Button(root, text="选择源目录", command=lambda: select_directory(src_label))
src_button.pack()

# 目标目录选择部分
dest_label = tk.Label(root, text="选择目标目录", width=50, anchor='w')
dest_label.pack(pady=10)

dest_button = tk.Button(root, text="选择目标目录", command=lambda: select_directory(dest_label))
dest_button.pack()

# 开始复制按钮
copy_button = tk.Button(root, text="开始复制并重命名", command=start_copying)
copy_button.pack(pady=20)

# 运行GUI
root.mainloop()
