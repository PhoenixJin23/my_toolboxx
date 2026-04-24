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

        if settings['watermark_mode']=="图片logo" and settings['logo_img']:
            logo=settings['logo_img'].copy() #避免原图作为logo被更改
            logo.thumbnail((150,150))
            logo_width,logo_height=logo.size
            offset=(current_width-logo_width-40,current_height-logo_height-40)
            img.paste(logo,offset,logo)

    return img 



