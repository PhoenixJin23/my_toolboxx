import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


def process_single_image(img,settings):
    """对单张图片按设置进行处理
       settings是字典，包含用户在网页上的所有选择"""

    #1.缩放
    if settings['do_resize']:
        target_width=settings['target_width']
        ratio=target_width/float(img.size[0])
        target_height=int(ratio*img.size[1])
        img=img.resize((target_width,target_height),Image.Resampling.LANCZOS)

    #2.水印
    if settings['watermark_mode']!="不添加水印":
        #重新获取当前图片尺寸
        current_width,current_height=img.size

        if settings['watermark_mode']=="文字水印":
            draw=ImageDraw.Draw(img)
            try:
                font=ImageFont.truetype("simhei.ttf",settings['font_size'])
            except:
                font=ImageFont.load_default()
            position=(current_width-180,current_height-80)
            draw.text(position,settings['watermark_text'],font=font,fill=(255,255,255,128))

        elif settings['watermark_mode']=="图片logo" and settings['logo_img']:
            logo=settings['logo_img'].copy() #避免原图作为logo被更改
            logo.thumbnail((150,150)) #把Logo缩放到最大150×150，保持比例不变形
            logo_width,logo_height=logo.size
            offset=(current_width-logo_width-40,current_height-logo_height-40)
            #Logo放在图片右下角，距离右边、底边各40像素
            img.paste(logo,offset,logo) #要贴的图片，要贴的位置，让logo透明背景生效

    return img


def run_image_tool():
    st.header("🖼️ 图片智能处理器")
    st.info("这里集合了各种图片处理逻辑")

    #A.路径设置
    st.subheader("1.路径设置")
    col_in,col_out=st.columns(2) #把一行切分成等宽的两部分（左右并排）
    with col_in:
        input_dir=st.text_input("输入文件夹","C:/Users/g3472/Desktop/cutiemice")
    with col_out:
        output_dir=st.text_input("输出文件夹","C:/Users/g3472/Desktop/cutiemice")

    #B.功能开关
    st.subheader("2.处理选项")

    c1,c2,c3=st.columns(3) #三个列并排放置开关

    with c1:
        do_resize=st.checkbox("启用放缩",value=True)
        target_width=st.number_input("目标宽度",value=1500) if do_resize else 1500

    with c2:
        watermark_mode=st.radio("水印模式",["不添加水印","文字水印","图片logo"])
        w_text=""
        l_img=None
        if watermark_mode=="文字水印":
            w_text=st.text_input("水印文字","watermark") #这里的watermark作为值是默认提示文字
        elif watermark_mode=="图片logo":
            l_path=st.text_input("Logo路径","C:/Users/g3472/Desktop/cutiemice")
            if os.path.exists(l_path):
                l_img=Image.open(l_path).convert("RGBA")

    with c3:
        out_format=st.selectbox("输出格式",["保持原样",".webp",".jpg",".png"])

    #C.执行处理
    if st.button("🚀 开始批量处理",type="primary"): #type="primary"让按钮使用主题的“主色”，让它成为页面里最显眼的按钮
        if not os.path.exists(input_dir):
            st.error("输入路径不存在！")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        #整理设置字典
        settings={
            'do_resize':do_resize,
            'target_width':target_width,
            'watermark_mode':watermark_mode,
            'watermark_text':w_text,
            'logo_img':l_img,
            'font_size':24
        }

        files=[f for f in os.listdir(input_dir) if f.lower().endswith(('.png','.jpg','.jpeg','.bmp'))]

        progress_bar=st.progress(0) #创建一个进度条，初始进度为0
        for i,filename in enumerate(files):
        #i是更新进度条必需元素，enumerate会自动给files里的文件从0开始依次编号
        #不能for i,filename in files:Python不知道i是什么
            try:
                img_path=os.path.join(input_dir,filename)
                with Image.open(img_path) as img:
                    #调用处理逻辑
                    processed_img=process_single_image(img,settings)
                    #处理文件名和格式
                    name_without_ext=os.path.splitext(filename)[0]
                    if out_format=="保持原样":
                        final_ext=os.path.splitext(filename)[1]
                    else:
                        final_ext=out_format

                    save_path=os.path.join(output_dir,name_without_ext+final_ext)

                    #如果是JPG，需要转成RGB模式（防止透明度报错）
                    if final_ext.lower() in ['.jpg','.jpeg']:
                        processed_img=processed_img.convert("RGB")

                    processed_img.save(save_path)

                progress_bar.progress((i+1)/len(files)) #更新进度
            except Exception as e:
                st.warning(f"跳过文件{filename}:{e}")

        st.success(f"🎉 处理完成！共处理{len(files)}张图片")



