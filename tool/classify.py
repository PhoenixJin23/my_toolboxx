import os
import streamlit as st

#task:扫描一个文件夹，根据文件的后缀名（如.jpg,.pdf,.py），自动把它们移动到对应的子文件夹里。

def classify_files(target_dir):
    #定义分类规则
    extension_rules={
        ".png":"images",
        ".jpg":"images",
        ".jpeg":"images",
        ".heic":"images",
        ".pdf":"documents",
        ".docx":"documents",
        ".txt":"documents",
        ".py":"python_scripts",
        ".zip":"archives"
    }

    #从目标文件夹中获取所有文件
    files=[f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir,f))]
    if not files:
        return "文件夹是空的，或者没有可分类的文件。"

    count=0
    log_placeholder=st.empty() #在网页留一块空间放日志
    log_text="" #日志内容

    for filename in files:
        #构造文件的完整路径（文件夹+文件名）
        old_path=os.path.join(target_dir,filename)
        # 获取文件后缀名：os.path.splitext
        _, extension = os.path.splitext(filename)
        extension = extension.lower()  # 后缀名全部转化为小写
        moved=False


        for folder_name,extension in extension_rules.items():
            if extension in extension_rules:
                folder_name=extension_rules[extension] #由后缀名对应文件类型
            else: #不在规则里，就去others
                folder_name="others"

            folder_path=os.path.join(target_dir,folder_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            #移动文件进行重新分类
            new_path=os.path.join(folder_path,filename)

            if not os.path.exists(new_path):
                os.rename(old_path,new_path)
                moved=True
                log_text+=f"移动成功！{filename}---->{folder_name}"
                count+=1
            break
        if not moved: #如果目标位置已经有同名文件了，先不移动，防止覆盖
            log_text+=f"跳过未知格式：{filename}"
    return f"分类完成！共处理了{count}个文件。"


def run_classify():
    st.header("📁 文件分类助手")
    st.info("提示：本工具将扫描目标文件夹，根据文件后缀进行分类")

    #用户输入
    target_dir=st.text_input("目标文件夹","eg:C:/Users/g3472/Desktop/cutiemice")

    #开始执行
    if st.button("开始分类","primary"):
        if not os.path.exists(target_dir):
            st.error("错误！请检查输入的地址！")
        else:
            with st.spinner("正在分类，请稍后..."):
                result=classify_files(target_dir)
                st.success(result)
                st.balloons()










