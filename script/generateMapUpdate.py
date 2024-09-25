import json
import os
from datetime import date

import pandas as pd

def get_map_full(directory):
    """
    获取指定目录下所有图片文件的文件名（不包含后缀）。

    :param directory: 目标目录路径
    :return: 包含图片文件名（不含后缀）的列表
    """
    # 图片文件的常见后缀
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp',".webp"]
    
    # 获取目录下所有文件名
    files = os.listdir(directory)
    # file_paths = 
    # for i in [os.path.join(directory, file) for file in files]:
    #     file_paths.append(i.replace("\\", "/"))
    # print(file_paths)
    # 过滤出图片文件，并移除后缀
    map_full = [os.path.splitext(file)[0] for file in files if os.path.splitext(file)[1].lower() in image_extensions]
    
    return map_full,files

def get_map_data_list_from_excel(excel_file_path):
    df_selected_columns = pd.read_excel(excel_file_path, usecols=['地图名称', '实际宽',"实际高","高度缩放","更新时间"])
    df_selected_columns['更新时间'] = df_selected_columns['更新时间'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df_selected_columns.values


if __name__ == '__main__':
    map_full,map_file_full = get_map_full("Maps\\full")
    map_lite,map_file_lite = get_map_full("Maps\\lite")
    map_height,map_height_file = get_map_full("Maps\\heightmap")

    map_data = get_map_data_list_from_excel("excel\\地图数据.xlsx")
    data_dict =  {}
    map_data_list = []
   
    if len(map_full) != len(map_data):
        
        print("地图数量不匹配",)
        exit(0)
    
    for i in range(len(map_full)):
        for j in range(len(map_data)):
            flag = False
            for k in range(len(map_height)):
                if map_full[i] == map_data[j][0] == map_lite[i] == map_height[k]:
                    print(f"正在匹配{map_full[i]} {len(map_data_list)+1}")
                    map_data_list.append({
                        "map_name":map_full[i] ,
                        "map_size":[max(int(map_data[j][1]),int(map_data[j][2])),max(int(map_data[j][1]),int(map_data[j][2])) ],
                        "update_time":map_data[j][4],
                        "map_pixmap_full_url":f"https://gitee.com/squadtools/squad-tools-repository/raw/master/Maps/full/{map_file_full[i]}",
                        "map_pixmap_lite_url":f"https://gitee.com/squadtools/squad-tools-repository/raw/master/Maps/lite/{map_file_lite[i]}",
                        "map_heightmap_url":f"https://gitee.com/squadtools/squad-tools-repository/raw/master/Maps/heightmap/{map_height_file[k]}",
                        "map_height_factor":map_data[j][3]
                    }) 
                    flag = True
                    break 
            if flag: 
                break
        
    data_dict["map_data_list"] = map_data_list     
    with open("Json/map_data.json","w",encoding="utf-8") as f: 
        json.dump(data_dict,f,ensure_ascii=False,indent=4)  
    print("生成地图数据成功 匹配数量：",len(map_data_list))

    
        
    

    

    



