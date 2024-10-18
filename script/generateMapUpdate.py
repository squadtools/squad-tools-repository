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
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]

    # 获取目录下所有文件名
    files = os.listdir(directory)
    # file_paths =
    # for i in [os.path.join(directory, file) for file in files]:
    #     file_paths.append(i.replace("\\", "/"))
    # print(file_paths)
    # 过滤出图片文件，并移除后缀
    map_full = [
        os.path.splitext(file)[0]
        for file in files
        if os.path.splitext(file)[1].lower() in image_extensions
    ]

    return map_full, files


def get_map_data_list_from_excel(excel_file_path):
    df_selected_columns = pd.read_excel(
        excel_file_path,
        usecols=[
            "地图名称_英文",
            "地图名称_中文",
            "实际宽",
            "实际高",
            "高度缩放",
            "更新时间",
        ],
    )
    df_selected_columns["更新时间"] = df_selected_columns["更新时间"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return df_selected_columns.values


if __name__ == "__main__":
    hostUrl = "https://gitee.com/squadtools/squad-tools-repository/raw/main"
    fullMapPath = "Maps/full"
    liteMapPath = "Maps/lite"
    heightMapPath = "Maps/heightmap"
    previewMapPath = "Maps/previews"
    excelPath = "excel\\地图数据.xlsx"

    # 获取地图文件名
    map_full, map_file_full = get_map_full(fullMapPath)
    map_lite, map_file_lite = get_map_full(liteMapPath)
    map_height, map_height_file = get_map_full(heightMapPath)
    map_preview, map_preview_file = get_map_full(previewMapPath)
    # 获取地图数据
    map_data = get_map_data_list_from_excel(excelPath)
    data_dict = {}
    map_data_list = []

    if len(map_full) != len(map_data):
        print("地图数量不匹配")
        exit(0)
    if len(map_preview) != len(map_data):
        print("预览图数量不匹配")
        exit(0)
    if len(map_lite)!= len(map_data):
        print("缩略图数量不匹配")
        exit(0)
    if len(map_height)!= len(map_data):
        print("高度图数量不匹配")
        exit(0)
    # 检查空列表
    # if not (map_full and map_data and map_lite and map_height and map_preview):
    #     print("其中一个或多个地图列表为空，无法进行匹配。")
    #     exit(0)

    # 使用字典存储 map_data 的信息
    map_data_dict = {data[0]: data for data in map_data}

    # 优化后的遍历逻辑
    for i, full_map in enumerate(map_full):
        
        if full_map not in map_data_dict:
            print(f"未找到 {full_map} 对应的数据，跳过当前项。")
            continue
            
        data = map_data_dict[full_map]
        name_en = data[0]
        name_zh = data[1]

        try:
            map_size = max(int(data[2]), int(data[3]))
        except ValueError:
            print(f"无法将 {data[2]} 或 {data[3]} 转换为整数，跳过当前项。")
            continue

        update_time = data[5]
        height_factor = data[4]

        # 查找对应的文件路径
        full_pix_url = f"{hostUrl}/{fullMapPath}/{map_file_full[i]}"
        lite_pix_url = f"{hostUrl}/{liteMapPath}/{map_file_lite[i]}"

        height_map_url = None
        for height_file in map_height:
            if height_file == full_map:
                height_map_url = f"{hostUrl}/{heightMapPath}/{map_height_file[map_height.index(height_file)]}"
                break
            

        preview_map_url = None
        for preview_file in map_preview:
            if preview_file == full_map:
                preview_map_url = f"{hostUrl}/{previewMapPath}/{map_preview_file[map_preview.index(preview_file)]}"
                break
            
        
        if height_map_url and preview_map_url:
            print(f"正在匹配 {full_map} {len(map_data_list) + 1}")
            map_data_list.append(
                {
                    "name_en": name_en,
                    "name_zh": name_zh,
                    "map_size": map_size,
                    "updateTime": update_time,
                    "fullPixUrl": full_pix_url,
                    "litePixUrl": lite_pix_url,
                    "heightmapUrl": height_map_url,
                    "previewMapUrl": preview_map_url,
                    "heightFactor": height_factor,
                }
            )

    data_dict["map_data_list"] = map_data_list
    with open("Json/map_data_update.json", "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
    print("生成地图数据成功 匹配数量：", len(map_data_list))
