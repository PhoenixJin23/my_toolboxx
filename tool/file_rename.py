import os
import json
import streamlit as st


# ==========================================
# 第一部分：核心逻辑函数
# ==========================================

def obfuscate_core(folder_path, key_path):
    # 1. 检查钥匙是否已存在
    if os.path.exists(key_path):
        return False, "错误：钥匙已存在，请先还原！"

    files = os.listdir(folder_path)
    name_map = {}
    count = 0

    for old_name in files:
        old_path = os.path.join(folder_path, old_name)

        # 2. 确保是文件且不是钥匙本身
        if os.path.isfile(old_path) and old_name != "key.json":
            new_name = f"secret_{count}.dat"
            new_path = os.path.join(folder_path, new_name)

            # 3. 执行重命名
            os.rename(old_path,new_path) #必须传入两个文件的完整路径，否则可能找不到文件

            # 4. 记录对应关系
            name_map[new_name] = old_name #键--值：新名--旧名
            count += 1

    # 5. 保存钥匙文件
    with open(key_path, "w", encoding="utf-8") as f:
        json.dump(name_map,f,ensure_ascii=False,indent=4) #*写入JSON文件


    return True, f"成功混淆 {count} 个文件！"


def restore_core(folder_path, key_path):
    # 1. 检查钥匙是否存在
    if not os.path.exists(key_path):
        return False, "找不到钥匙文件！"

    # 2. 读取钥匙
    with open(key_path, "r", encoding="utf-8") as f:
        name_map=json.load(f) #*读取JSON

    # 3. 遍历字典还原
    for secret_name,original_name in name_map.items():
        current_path = os.path.join(folder_path, secret_name)
        original_path = os.path.join(folder_path, original_name)

        if os.path.exists(current_path):
            os.rename(current_path, original_path)

    # 4. 任务完成后删除钥匙
    os.remove(key_path)  #*删除文件函数
    return True, "所有文件已还原！"


# ==========================================
# 第二部分：网页界面函数
# ==========================================

def run_obfuscator():
    # 1. 获取路径
    target_dir = st.text_input("请输入目标文件夹路径")  # 填空：文本输入组件

    # 2. 钥匙存放位置（固定在桌面）
    key_path = os.path.join("C:/Users/g3472/Desktop", "key.json")

    # 3. 选择模式
    mode = st.radio("请选择操作模式", ["混淆文件", "还原文件"]) #*单选框组件radio,折叠款selectbox

    # 4. 执行按钮
    if st.button("🚀 执行操作"):  # 填空：按钮组件
        if not os.path.exists(target_dir):
            st.error("文件夹路径不存在！")
        else:
            if mode == "混淆文件":
                success, msg = obfuscate_core(target_dir, key_path)
            else:
                success, msg = restore_core(target_dir, key_path)

            # 5. 根据结果显示反馈
            if success:
                st.success(msg)  # 填空：成功提示组件
            else:
                st.error(msg)  # 填空：错误提示组件