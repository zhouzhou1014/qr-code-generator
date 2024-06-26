#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2024/6/21 21:36
# @Author  : zhouzhou
# @File    : qrCodeGeneration_demo.py
# @Software: PyCharm

from common.my_execl import MyExcel
from common.my_path import logos_path, BasicData_path, QRCodes_path, fonts_path
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os


# 生成普通二维码
def generate_qr_code(fileName, qr_size):
    # 定义文件路径，该路径指向一个Excel文件，用于后续读取工作表名称
    file_path = os.path.join(BasicData_path, fileName)

    # 调用get_sheet_names函数获取Excel文件中所有工作表的名称
    sheet_names = MyExcel().get_sheet_names(file_path)

    # 遍历所有工作表名称，对每个工作表读取其数据
    for sheet_name in sheet_names:
        # 使用MyExcel类的read_data方法读取指定工作表的数据
        data_list = MyExcel().read_data(file_path, sheet_name)
        # 打印读取的数据，用于检查数据是否正确读取
        # print(data_list)

        for item in data_list:
            # 创建二维码对象
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            # 添加数据到二维码对象
            qr.add_data(item['二维码链接'])
            qr.make(fit=True)
            # 生成二维码图像
            img = qr.make_image(fill_color="black", back_color="white")
            # 控制生成二维码的大小
            img = img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

            # 获取文件的目录
            directory = os.path.join(QRCodes_path, str(item['店铺ID']))

            # 如果目录不存在，则创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 将二维码图像保存到指定路径
            file_path_png = os.path.join(directory, f"{item['店铺ID']}_{item['桌台名称']}.png")
            img.save(file_path_png)
            print(f"二维码已保存到 {file_path_png}")


# 带有logo的二维码
def add_logo_to_qr(img, logo_path):
    logo = Image.open(logo_path)

    # 将Logo剪裁为圆形
    # mask = Image.new('L', logo.size, 0)
    # draw = ImageDraw.Draw(mask)
    # draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)

    # 确保 logo 是 RGBA 模式
    logo = logo.convert("RGBA")
    # mask = mask.convert("L")

    # 调整Logo大小
    # logo_width, logo_height = logo.size
    # qr_width, qr_height = img.size
    # factor = 4  # 控制Logo大小的比例因子
    # size = (qr_width // factor, qr_height // factor)
    # logo = logo.resize(size, Image.Resampling.LANCZOS)
    # mask = mask.resize(size, Image.Resampling.LANCZOS)
    # 调整Logo大小
    logo_width, logo_height = logo.size
    qr_width, qr_height = img.size
    factor = 4  # 控制Logo大小的比例因子
    size = (qr_width // factor, qr_height // factor)
    logo = logo.resize(size, Image.Resampling.LANCZOS)

    # 将Logo粘贴到二维码中心
    pos = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
    img.paste(logo, pos, logo)


def generate_qr_code_with_logo(data, logo_path, save_path, qr_size):
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # 添加数据到二维码对象
    qr.add_data(data)
    qr.make(fit=True)
    # 生成二维码图像
    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # 调整二维码图像大小
    img = img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # 添加Logo到二维码
    add_logo_to_qr(img, logo_path)

    # 保存二维码图像到指定路径
    img.save(save_path)
    print(f"二维码已保存到 {save_path}")


def generate_qr_code_with_logo_text(data, logo_path, save_path, qr_size, text, font_name):
    """
    生成带有Logo和文本的二维码
    :param data: 二维码数据
    :param logo_path: Logo文件路径
    :param save_path: 保存二维码文件的路径
    :param qr_size: 二维码图像大小
    :param text: 要添加的文本
    :param font_name: 文本字体名称
    """
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # 添加数据到二维码对象
    qr.add_data(data)
    qr.make(fit=True)
    # 生成二维码图像
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # 调整二维码图像大小
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # 添加Logo到二维码
    add_logo_to_qr(qr_img, logo_path)

    # 创建一个新的图像，包含二维码和文本
    total_height = qr_size + 20  # 给文本留出空间，20像素可以根据需要调整
    img = Image.new('RGBA', (qr_size, total_height), 'white')
    img.paste(qr_img, (0, 0))

    # 在图像下方添加文本
    draw = ImageDraw.Draw(img)

    # 20 字体大小
    font = ImageFont.truetype(os.path.join(fonts_path, font_name), 20)

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (qr_size - text_width) // 2
    text_y = qr_size - 15  # 在二维码下方-10像素处开始绘制文本
    draw.text((text_x, text_y), text, font=font, fill="black")

    # 保存最终图像
    img.save(save_path)
    print(f"二维码已保存到 {save_path}")


def generate_qr_codes(fileName, qr_size, logo_name):
    # 定义文件路径，该路径指向一个Excel文件，用于后续读取工作表名称
    file_path = os.path.join(BasicData_path, fileName)

    # 调用get_sheet_names函数获取Excel文件中所有工作表的名称
    sheet_names = MyExcel().get_sheet_names(file_path)
    logo_path = os.path.join(logos_path, logo_name)  # 上传的Logo文件路径
    # qr_size = qr_size  # 二维码图像大小

    for sheet_name in sheet_names:
        data_list = MyExcel().read_data(file_path, sheet_name)
        for item in data_list:
            data = item['二维码链接']
            directory = os.path.join(QRCodes_path, str(item['店铺ID']))
            # 如果目录不存在，则创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)

            save_path = os.path.join(directory, f"{item['店铺ID']}_{item['桌台名称']}.png")
            generate_qr_code_with_logo(data, logo_path, save_path, qr_size)


# 带有logo和文本的二维码
def generate_qr_codes_text(fileName, qr_size, logo_name, font_name):
    """
    生成带有Logo和文本的二维码
    :param fileName: Excel文件名
    :param qr_size: 二维码图像大小
    :param logo_name: Logo文件名
    :param font_name: 文本字体名称
    """
    # 定义文件路径，该路径指向一个Excel文件，用于后续读取工作表名称
    file_path = os.path.join(BasicData_path, fileName)

    # 调用get_sheet_names函数获取Excel文件中所有工作表的名称
    sheet_names = MyExcel().get_sheet_names(file_path)
    logo_path = os.path.join(logos_path, logo_name)  # 上传的Logo文件路径

    for sheet_name in sheet_names:
        data_list = MyExcel().read_data(file_path, sheet_name)
        for item in data_list:
            data = item['二维码链接']
            text = item['二维码备注']
            directory = os.path.join(QRCodes_path, sheet_name)

            # 如果目录不存在，则创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)

            save_path = os.path.join(directory, f"{item['二维码备注']}.png")
            generate_qr_code_with_logo_text(data, logo_path, save_path, qr_size, text, font_name)


def qr_code_generation(qrCodeStatus, fileName, qr_size, logo_name=None, font_name=None):
    """
    二维码生成
    :param qrCodeStatus: 二维码生成方式
    :param fileName: Excel文件名
    :param qr_size: 二维码图像大小
    :param logo_name: Logo文件名
    :param font_name: 文本字体名称
    """
    if qrCodeStatus == 1:
        generate_qr_codes(fileName, qr_size, logo_name)
    elif qrCodeStatus == 2:
        generate_qr_codes_text(fileName, qr_size, logo_name, font_name)
    elif qrCodeStatus == 3:
        generate_qr_code(fileName, qr_size)
    else:
        print("请选择正确的二维码生成方式")


qr_code_generation(2, 'shop_01.xlsx', 300, '1.png', 'simhei.ttf')
