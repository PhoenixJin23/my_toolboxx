import os
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st

def merge_pdfs_core(folder_path,output_name,password=None):
    writer=PdfWriter()

    #获取目标文件夹下的所有PDF文件
    files=[f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    files.sort()

    if not files:
        return False,"文件夹里没有PDF文档哦！" #失败，返回False和错误原因

    #逐个读取并加入合并器
    for file in files:
        file_path=os.path.join(folder_path,file)
        reader=PdfReader(file_path)

        #将每一页都添加到writer里
        for page in reader.pages:
            writer.add_page(page)

    #如果设置了密码，进行加密
    if password:
        writer.encrypt(password)

    if not output_name.lower().endswith(".pdf"):
        output_name+=".pdf"

    #保存最终文件
    output_path=os.path.join(folder_path,output_name)
    with open(output_path,"wb") as f:
        writer.write(f)

    return True,output_path


def run_pdf_tool():
    st.header("📄 PDF合并与加密助手")
    st.info("提示：本工具将合并指定文件夹内所有PDF文件")

    #A.输入设置
    col1,col2=st.columns(2)
    with col1:
        folder_path=st.text_input("PDF文件夹路径","C:/Users/你的用户名/Desktop/pdfs")
    with col2:
        output_name=st.text_input("合并后的文件名","merged_document.pdf")

    #B.加密设置
    st.subheader("安全设置")
    enable_encryption=st.checkbox("启用密码加密")
    password=""
    if enable_encryption:
        #type="password"会让输入内容变成星号
        password=st.text_input("设置访问密码",type="password",help="合并后的PDF需要此密码才能打开")

    #C.执行按钮
    if st.button("🚀 开始合并PDF",type="primary"):
        if not os.path.exists(folder_path):
            st.error("❌ 路径不存在，请检查输入！")
        else:
            with st.spinner("正在合并中，请稍后..."):
                success,result=merge_pdfs_core(folder_path,output_name, password if enable_encryption else None)
                #merge_pdfs_core()返回True/False,output_name/错误原因（success和result组合使用）
                if success:
                    st.success(f"✅ 大功告成！")
                    st.balloons() #完结撒花
                    st.write(f"文件已保存在：{result}")
                else:
                    st.warning(result)





