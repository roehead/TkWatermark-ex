#!/usr/bin/python
# -*- coding:utf-8 -*-
#module watermark.py
# @Date    : 2017-12-29 13:29:07
# @Author  : cfq (cfqpeter@qq.com)
# @Link    : ${link}
# @Version : $1.0$

from PIL import Image
from PIL import ImageDraw, ImageFont
from LayerBlend import *
import numpy as np

IM_MOD= 'RGBA'

def fill_blank_for(blank_im):
    im_np = np.array(blank_im)
    for i in range(blank_im.size[1]):
        for j in range(blank_im.size[0]):
            if (im_np[i, j, 0] == 0 and im_np[i, j, 1] == 0 and im_np[i, j, 2] == 0):
                im_np[i, j, 0] = 255
                im_np[i, j, 1] = 255
                im_np[i, j, 2] = 255
    return Image.fromarray((im_np).astype('uint8')).convert(IM_MOD)

def fill_blank(blank_im,fill_color=(255, 255, 255, 0)):
    # 创建一个与旋转图像大小相同的白色图像
    layer_im = Image.new('RGBA', blank_im.size, fill_color)
    # 使用alpha层的mark_im 作为掩码创建一个复合图像
    return Image.composite(blank_im, layer_im, blank_im)

def rndColor():
    # return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255), 90)
    return (255, 0, 0, 255)

def watermark_txt_only(s, m, path=None, image=None):
    if path:
        im = Image.open(path).convert(IM_MOD)
    if image:
        im = image
    # w, h = im.size
    txt_im = Image.new(IM_MOD, im.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(txt_im)
    font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 40)
    if m:
        txt_im = m.resize(im.size)

    for c in range(len(s)):
        draw.text((30 * c + 100, 200), s[c], font=font, fill=rndColor())
    # out = Image.alpha_composite(im, txt_im)  # 融合
    out = Image.blend(im, txt_im, 0.8)  # 混合
    return out

def watermark(mark, mark_pos=(0,0),angle=60 ,path=None, image=None):
    def num_box(mark):
        width_num = 284
        height_num = 240.1
        num_start = int(mark)
        num_col = (num_start - 1) % 15
        num_row = (num_start - 1) // 15
        blank_top = 54
        blank_left = 232
        num_left = int(blank_left + num_col * width_num) + 18
        num_top = int(blank_top + num_row * height_num) + 13
        num_right = int(blank_left + num_col * width_num + width_num) - 8
        num_bottom = int(blank_top + num_row * height_num + height_num) - 6
        return (num_left,num_top,num_right,num_bottom)

    def paste_num(num_txt,txt_im,num_size,num_position,layer_im,mark_im):
        num_im = txt_im.crop(num_box(int(num_txt)))
        num_im = num_im.resize(num_size)

        #num_im = num_im.rotate(45,expand=0)
        #num_im = fill_blank(num_im,(255, 255, 255, 0))

        #num_im = um_im.crop(num_box(int(num_txt)))

        numadd_im = layer_im
        numadd_im.paste(num_im, num_position)

        if mark_im:
            np_numadd = np.array(numadd_im) / 255.0
            np_mark = np.array(mark_im) / 255.0
            mark_np = Multiply(np_mark, np_numadd)
            markimage = Image.fromarray((mark_np * 255.0).astype('uint8')).convert(IM_MOD)
        else:
            markimage = numadd_im

        return markimage

    if path:
        #markimage = Image.open(path).convert('RGBA')
        mark_filename = path
    if image:
        im = image
    if im.mode != IM_MOD:
        im = im.convert(IM_MOD)


    txt_im = Image.open(mark_filename).convert(IM_MOD)
    #width_num = 284 - 18 -8
    #height_num = 240.1 -13 -6

    num_size = (int(258*0.5),int(221*0.5))

    layer_im = Image.new(IM_MOD, (int(num_size[0]*1.6),int(int(num_size[1]*1.0))), (255, 255, 255, 255))   #不能透明
    w, h = layer_im.size
    print(w,h)

    z=int(num_size[0]/2.0)
    x=0
    y=0 #-10

    print(x,y,z)

   #-----------------------------------------------------------
    #paste_num( num_txt, txt_im, num_size, num_position, layer_im,mark_im)
    mark_im = layer_im #None
    if len(mark)>3 and mark[2]+mark[3] == '32':   #日期
        if  len(mark)>1:
          mark_im = paste_num( mark[0]+mark[1], txt_im, num_size, (x, y), layer_im,mark_im)
        if len(mark)>3:
          mark_im = paste_num( mark[2]+mark[3], txt_im, num_size, (int(x+0.7*z), y), layer_im,mark_im)
        if len(mark)>5:
          mark_im = paste_num( mark[4]+mark[5], txt_im, num_size, (int(x+1.6*z), y), layer_im,mark_im)
    else:  #非日期
        if  len(mark)>0:
          mark_im = paste_num( str(int((10-int(mark[0]))/10)*10+int(mark[0])+150), txt_im, num_size, (x, y), layer_im,mark_im)
        if len(mark)>1:
          mark_im = paste_num( str(int((10-int(mark[1]))/10)*10+int(mark[1])+150), txt_im, num_size, (int(x+0.8*z), y), layer_im,mark_im)
        if len(mark)>2:
          mark_im = paste_num( str(int((10-int(mark[2]))/10)*10+int(mark[2])+150), txt_im, num_size, (int(x+1.4*z), y), layer_im,mark_im)

    #mark_im = make_date(num_size)
    #mark_im = make_num(num_size)
    # ----------------------------------------------------------------------------------
    mark_im = mark_im.rotate(angle,resample=0, expand=1).convert(IM_MOD)
    # mark1_im = mark_im #debug
    mark_im = fill_blank(mark_im, (255, 255, 255, 255))
    #mark2_im = mark_im #debug


    layer_im = Image.new(IM_MOD, im.size, (255, 255, 255, 255))
    w, h = mark_im.size
    x = int(mark_pos[0]-w/2)
    y = int(mark_pos[1]-h/2)
    print(x, y)
    layer_im.paste(mark_im, (x,y))
    #mark3_im = layer_im  #debug

    #mark_im = fill_blank(layer_im, (255, 255, 255, 255))
    mark_im = layer_im

    #print(mark_im.size)
    #im = layer_im
    #out = Image.alpha_composite(im, txt_im)  # 融合

    # ----------------------------------------------------------------------------------
    im_np = np.array(im)/255.0
    mark_np = np.array(mark_im)/255.0
    #Dark2(im_np, mark_np)
    #alpha = 0.5
    #out_np = Transparent(im_np, mark_np, alpha)
    #out_np = Dark2(im_np, mark_np)
    out_np = Multiply (im_np, mark_np)
    #out_np = Color_burn(im_np, mark_np)
    #out_np = Color_dodge(im_np, mark_np)
    #out_np = Linear_burn(im_np, mark_np)
    #out_np = Linear_dodge(im_np, mark_np)
    #out_np = Lighten(im_np, mark_np)
    #out_np = Dark(im_np, mark_np)
    #out_np = Screen(im_np, mark_np)
    #out_np = Overlay(im_np, mark_np)
    #out_np = Soft_light(im_np, mark_np)
    #out_np = Hard_light(im_np, mark_np)
    #out_np = Vivid_light(im_np, mark_np)
    #out_np = Pin_light(im_np, mark_np)
    #out_np = Linear_light(im_np, mark_np)
    #out_np = Hard_mix(im_np, mark_np)

    out = Image.fromarray((out_np*255.0).astype('uint8')).convert(IM_MOD)
    print("ok!")
    return out
    #return mark3_im

#module watermark.py

