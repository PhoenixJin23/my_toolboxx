import os
from PIL import Image,ImageDraw,ImageFont #Python最流行的图像处理库


#创建/打开output_dir--->遍历input_dir--->检查后缀，只处理图片--->
#打开图片--->缩放图片--->添加水印（确定水印位置，设置字体、大小、颜色）--->
#绘制文字---->保存结果


def batch_process_images(input_dir, output_dir):
    #创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("---水印模式选择---")
    print("1:手动输入文字水印(DrawText)")
    print("2:使用已有图片Logo(PasteImage)")
    mode=input("请选择模式(输入1或2):")

    watermark_text=""
    logo_img=None

    if mode=="1":
        watermark_text=input("请输入要显示的水印文字: ")
    elif mode=="2":
        logo_path=input("请输入Logo图片的路径（完整路径，不带引号，用/分隔）:")
        if os.path.exists(logo_path):
            logo_img=Image.open(logo_path).convert("RGBA")
            logo_img.thumbnail((150, 150))  # 预缩放 Logo
        else:
            print("找不到Logo文件，将自动切换为文字模式。")
            mode="1"
            watermark_text="Default Watermark"


    #遍历文件夹
    for filename in os.listdir(input_dir):
        #检查后缀，只处理图片
        if filename.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
            img_path=os.path.join(input_dir,filename)

            try:
                #打开图片
                with Image.open(img_path) as img:
                    #缩放图片（保持比例）
                    #设定目标宽度为1500像素
                    target_width=1500
                    #计算缩放比例：目标宽度/原始宽度
                    ratio=target_width/float(img.size[0])
                    #计算对应高度
                    target_height=int(float(img.size[1])*ratio)
                    #执行缩放
                    img=img.resize((target_width,target_height),Image.Resampling.LANCZOS) #缩小图片时保证清晰

                    if mode=="1":
                        #添加水印
                        #首先创建一个画笔工具并绑定在img上（在img要进行绘图），得到的draw是画笔对象
                        draw=ImageDraw.Draw(img)

                        #加载字体
                        try:
                            font=ImageFont.truetype("simhei.ttf",24)
                        except:
                            font=ImageFont.load_default() #如果找不到黑体，用默认

                        #确认水印位置
                        position=(img.size[0]-180,img.size[1]-80) #宽度，高度

                        #绘制文字（颜色为白色，RGBA格式）A是透明度（0-255）
                        #draw.text()开始用“画笔”写字
                        draw.text(position,watermark_text,font=font,fill=(255,255,255,128))

                    elif mode=="2" and logo_img:
                        # 计算右下角位置
                        logo_w,logo_h=logo_img.size
                        logo_offset=(target_width-logo_w-40,target_height-logo_h-40)

                        # 使用logo自身的透明通道作为mask
                        img.paste(logo_img,logo_offset,logo_img)


                    #格式转换与保存 (转为 WebP 格式，体积更小)
                    file_name=os. path.splitext(filename)[0]+".webp"
                    save_path=os.path.join(output_dir,file_name)
                    img.save(save_path)
                    #print(f"处理成功:{file_name}")

            except Exception as e:
                print(f"处理{filename} 失败{e}")


batch_process_images("C:/Users/g3472/Desktop/cutiemice/images","C:/Users/g3472/Desktop/cutiemice/output4")

