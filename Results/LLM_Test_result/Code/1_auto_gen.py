import os
import shutil

def move_files_to_folders():
    # 获取当前目录下的所有文件和文件夹
    items = os.listdir('.')
    
    for item in items:
        # 跳过.py文件和目录
        if item.endswith('.py') or os.path.isdir(item):
            continue
        
        # 获取文件名（不带扩展名）和扩展名
        filename, ext = os.path.splitext(item)
        
        # 检查同名文件夹是否已存在
        if not os.path.exists(filename):
            # 创建新文件夹
            os.makedirs(filename)
            print(f"创建文件夹: {filename}")
        
        # 移动文件到同名文件夹
        src = item
        dst = os.path.join(filename, item)
        shutil.move(src, dst)
        print(f"移动文件: {item} -> {dst}")

if __name__ == "__main__":
    move_files_to_folders()
    print("操作完成！")