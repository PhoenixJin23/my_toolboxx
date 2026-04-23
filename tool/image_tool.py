import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 第一部分：核心逻辑函数 (从原来的脚本搬过来)
# 注意：删掉了所有的 input() 和 print()
# ==========================================
def batch_process_images_core(input_dir, output_dir, mode, watermark_text, logo_path):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logo_img = None
    if mode == "图片Logo" and logo_path:
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).convert("RGBA")
            logo_img.thumbnail((150, 150))

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            img_path = os.path.join(input_dir, filename)
            try:
                with Image.open(img_path) as img:
                    # 缩放逻辑
                    target_width = 1500
                    ratio = target_width / float(img.size[0])
                    target_height = int(float(img.size[1]) * ratio)
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                    if mode == "文字水印":
                        draw = ImageDraw.Draw(img)
                        try:
                            font = ImageFont.truetype("simhei.ttf", 24)
                        except:
                            font = ImageFont.load_default()
                        position = (img.size[0] - 180, img.size[1] - 80)
                        draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

                    elif mode == "图片Logo" and logo_img:
                        logo_w, logo_h = logo_img.size
                        logo_offset = (target_width - logo_w - 40, target_height - logo_h - 40)
                        img.paste(logo_img, logo_offset, logo_img)

                    # 保存
                    file_name = os.path.splitext(filename)[0] + ".webp"
                    save_path = os.path.join(output_dir, file_name)
                    img.save(save_path)
            except Exception as e:
                st.error(f"处理 {filename} 失败: {e}")

# ==========================================
# 第二部分：网页界面函数 (专门给 Streamlit 用)
# ==========================================
def run_image_tool():
    st.header("📸 批量图片水印工具")

    # 1. 路径输入
    input_dir = st.text_input("输入图片文件夹路径", "C:/Users/你的用户名/Desktop/images")
    output_dir = st.text_input("输出结果文件夹路径", "C:/Users/你的用户名/Desktop/output")

    # 2. 模式选择 (替代原来的 input("请选择模式"))
    mode = st.radio("选择水印模式", ["文字水印", "图片Logo"])

    watermark_text = ""
    logo_path = ""

    if mode == "文字水印":
        watermark_text = st.text_input("请输入水印文字", "My Watermark")
    else:
        logo_path = st.text_input("请输入 Logo 图片的完整路径(不带引号)", "C:/logo.png")

    # 3. 开始按钮
    if st.button("🚀 开始批量处理"):
        if not os.path.exists(input_dir):
            st.error("输入路径不存在，请检查！")
        else:
            with st.spinner("正在处理中，请稍候..."):
                # 调用上面的核心逻辑函数
                batch_process_images_core(input_dir, output_dir, mode, watermark_text, logo_path)
            st.success(f"✅ 处理完成！文件已保存至: {output_dir}")