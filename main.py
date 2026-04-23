"""import streamlit as st
from tool.image_processor import batch_process_images



# 1. 设置侧边栏菜单
st.sidebar.title("🛠️ Python 万能工具箱")
menu = st.sidebar.radio(
    "请选择一个工具：",
    ("首页介绍", "图片水印助手", "PDF 合并工具", "账单分析仪")
)

# 2. 根据菜单选择，显示不同的内容
if menu == "首页介绍":
    st.title("欢迎来到我的 Python 工具箱")
    st.write("这是我学习 Python 以来积累的所有自动化工具。")
    st.info("请在左侧选择你想要使用的功能。")

elif menu == "图片水印助手":
    st.title("📸 图片水印助手")
    st.write("这里将集成你之前的图片处理逻辑...")
    batch_process_images("C:/Users/g3472/Desktop/cutiemice/images","C:/Users/g3472/Desktop/cutiemice/output4")


elif menu == "PDF 合并工具":
    st.title("📄 PDF 合并工具")
    st.write("这里将集成你之前的 PDF 合并逻辑...")

elif menu == "账单分析仪":
    st.title("💰 账单分析仪")
    st.write("这里将集成你之前的账单分析逻辑...")
    """
import streamlit as st
from tool.image_tool import run_image_tool

st.sidebar.title("🛠️ Python 工具箱")
choice = st.sidebar.selectbox("请选择工具", ["首页", "图片水印工具"])

if choice == "首页":
    st.title("欢迎使用我的工具箱")
elif choice == "图片水印工具":
    run_image_tool()