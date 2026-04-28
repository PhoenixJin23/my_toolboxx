import os
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

#设置中文字体（防止绘图时中文乱码，Windows通用）
plt.rcParams['font.sans-serif']=['SimHei']

def get_folder_size(folder_path): #folder_path是target_dir下属文件夹的路径
    """计算一个文件夹的总大小（工具函数，被主程序调用）"""
    total_size=0
    try:
        #os.walk返回 路径、文件夹名列表、文件名列表（递归的“深度搜索”）
        for dirpath,dirnames,filenames in os.walk(folder_path):
            for f in filenames:
                fp=os.path.join(dirpath,f)
                #累加每个文件的大小
                if os.path.exists(fp):
                    total_size+=os.path.getsize(fp)
                    #getsize返回的是字节，1KB=1024Byte，1MB=1024KB
    except Exception as e:
        st.error(f"读取{folder_path}出错：{e}")
    return total_size/(1024*1024) #换算成MB


def run_folder_analyzer():
    st.header("📊 文件夹空间扫描仪")

    target_dir=st.text_input("请输入要扫描的文件夹路径：","eg:C:/Users/g3472/Desktop/cutiemice")

    if st.button("开始扫描",type="primary"):
        if not os.path.exists(target_dir):
            st.error("路径不存在！")
            return

        with st.spinner("正在深度扫描文件夹，请稍后..."):
            folder_names=[]
            folder_sizes=[]

            #获取目标目录下所有的子文件夹
            items=os.listdir(target_dir) #返回目标文件夹包含的文件（夹）名字列表，只能看到第一层文件（夹）
            for item in items:
                item_path=os.path.join(target_dir,item)
                if os.path.isdir(item_path):
                    #计算每个子文件夹的大小
                    size=get_folder_size(item_path) #调用get_folder_size()这个工具函数
                    if size>0.1: #只记录大于0.1MB的文件夹，防止图表太乱
                        folder_names.append(item)
                        folder_sizes.append(size)

        if not folder_sizes:
            st.warning("没有发现足够大的子文件夹（>0.1MB）")
        else:
            st.subheader("分析结果")
            fig,ax=plt.subplots(figsize=(10,7))#设置画布大小和坐标轴
            plt.pie(folder_sizes,labels=folder_names,autopct='%1.1f%%',startangle=140)
            plt.title(f"文件夹空间占用分析：{target_dir}")
            plt.axis('equal') #保证饼图是圆的

            st.pyplot(fig) #不用plt.show()，不需要服务端弹出窗口，也避免部署到云端时程序卡死

            st.subheader("详细数据表格")
            df=pd.DataFrame({
                "文件夹名称":folder_names,
                "占用空间(MB)":folder_sizes
            }).sort_values(by="占用空间(MB)",ascending=False)
            st.table(df)





