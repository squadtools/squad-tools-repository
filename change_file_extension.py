import os
import shutil

def change_file_extension(directory, old_extension, new_extension):
    """
    更改指定目录下所有特定后缀文件的后缀名。
    
    :param directory: 目录路径
    :param old_extension: 原文件后缀（包括点，如'.txt'）
    :param new_extension: 新文件后缀（包括点，如'.md'）
    """
    for filename in os.listdir(directory):
        # 确保是文件且文件后缀匹配
        if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(old_extension):
            # 构建新文件名
            new_filename = filename[:-len(old_extension)] + new_extension
            # 构建完整的旧文件路径和新文件路径
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)
            # 使用shutil.move来重命名文件，实际上就是改变后缀
            shutil.move(old_filepath, new_filepath)
            print(f'{filename} -> {new_filename}')

# 使用示例
directory_path = 'heightmap_raw'  # 替换为你的目录路径
old_ext = '.mapdata'
new_ext = '.png'

change_file_extension(directory_path, old_ext, new_ext)



