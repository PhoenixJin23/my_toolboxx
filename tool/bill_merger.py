"""
统一格式：微信的金额列叫“金额(元)”，支付宝的叫“金额”。我们要把它们统一改名为“金额”。
清洗杂质：账单里有很多“转账”、“还款”、“收入”。如果我们只想看支出，就要根据“收/支”这一列，过滤掉所有不等于“支出”的行。
处理日期：微信的日期可能是 2023-03-01 12:00:00，我们要用 pd.to_datetime 把它们转换成标准的日期格式，方便后续按日期排序。
合并数据：使用 Pandas 的 pd.concat([df1, df2]) 函数，把两张表像叠罗汉一样叠在一起。
导出结果：在网页上，我们不能直接写 df.to_csv("path")，因为那是存到服务器了（也就是我的电脑里）。我们要把处理好的数据转换成字节流，让用户通过“download_button按钮”下载到自己电脑上。
"""

import pandas as pd
import streamlit as st
import io


def process_bills(wechat_file, alipay_file):
    # --- 1. 处理微信账单 ---
    # 微信通常前16行是统计说明，需要跳过
    df_wechat = pd.read_csv(wechat_file, skiprows=17)  #指定跳过行数

    # 筛选支出，统一列名
    df_wechat = df_wechat[df_wechat['收/支'] == '支出']
    df_wechat = df_wechat[['交易时间', '商品', '收/支', '金额(元)', '交易对方']]
    df_wechat.columns = ['日期', '商品', '类型', '金额', '对方']

    # --- 2. 处理支付宝账单 ---
    # 支付宝通常是 GBK 编码，且前几行也要跳过
    df_alipay = pd.read_csv(alipay_file, encoding='utf-8', skiprows=24)  #常见的中文编码名
    df_alipay.columns = [c.strip() for c in df_alipay.columns]
    # 筛选支出，统一列名
    df_alipay = df_alipay[df_alipay['收/支'] == '支出']
    df_alipay = df_alipay[['交易时间', '商品说明', '收/支', '金额', '交易对方']]
    df_alipay.columns = ['日期', '商品', '类型', '金额', '对方']


    # --- 3. 合并与排序 ---
    combined_df = pd.concat([df_wechat, df_alipay])  #合并函数
    combined_df['日期'] = pd.to_datetime(combined_df['日期'],format="mixed", dayfirst=False)  #转换日期函数
    combined_df = combined_df.sort_values(by='日期', ascending=False)

    return combined_df


def run_bill_converter():
    st.header("💰 账单一键合并工具")
    st.write("上传微信和支付宝导出的原始 CSV，直接获取合并后的标准账单。")

    # 1. 文件上传组件
    col1, col2 = st.columns(2)
    with col1:
        wechat_file = st.file_uploader("上传微信账单 (CSV)", type=['csv'])  #*上传组件
    with col2:
        alipay_file = st.file_uploader("上传支付宝账单 (CSV)", type=['csv'])

    if wechat_file and alipay_file:
        if st.button("🚀 开始合并"):
            try:
                result_df = process_bills(wechat_file, alipay_file)

                # 2. 展示预览
                st.subheader("合并预览 (前5行)")
                st.dataframe(result_df.head())  #展示表格

                # 3. 导出下载 (Streamlit 特色逻辑)
                csv_buffer = io.StringIO()
                result_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 下载合并后的账单",
                    data=csv_buffer.getvalue(),
                    file_name="merged_bill.csv",
                    mime="text/csv"
                )  # 填空：下载按钮组件
            except Exception as e:
                st.error(f"处理出错：{e}")