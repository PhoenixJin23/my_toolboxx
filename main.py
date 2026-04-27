import streamlit as st
from tool.image_tool import run_image_tool
from tool.pdf_tool import run_pdf_tool
from tool.classify import run_classify



# 1. 设置侧边栏菜单
st.sidebar.title("🛠️ Python 万能工具箱")
menu = st.sidebar.radio(
    "请选择一个工具：",
    ("首页介绍", "图片处理助手", "PDF合并工具", "文件分类器","账单分析仪")
)

# 2. 根据菜单选择，显示不同的内容
if menu == "首页介绍":
    st.title("欢迎来到我的 Python 工具箱")
    st.write("这是我学习 Python 以来积累的所有自动化工具。")
    st.info("请在左侧选择你想要使用的功能。")

elif menu == "图片处理助手":
    run_image_tool()

elif menu == "PDF合并工具":
    run_pdf_tool()

elif menu == "文件分类器":
    run_classify()

elif menu == "账单分析仪":
    st.title("💰 账单分析仪")
    st.info("这里集成了账单分析逻辑...")



#✨ 📸 🎯 🎨 📁 📝 ✅ ❌ 🚀 💡 🖼️ 🔥
#🌟 🎉 📊 📌 🔒 🔍 📎 🎧 🍉 📷 💻