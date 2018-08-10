#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-29 13:29:07
# @Author  : cfq (cfqpeter@qq.com)
# @Link    : ${link}
# @Version : $1.0$

#from TKinter inport * #fro python 2.7
from tkinter import *
from PIL import Image, ImageTk
#from PIL import ImageDraw, ImageFont,ImageEnhance  # for python2.7
#import numpy as np # for python2.7
#import tkMessageBox as messagebox     # for python2.7
#import tkFileDialog as filedialog  # for python2.7
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

# import random

from watermark import *

IM_MOD= 'RGBA'

class watermark_App(Frame):   #应用程序类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):  #创建控件
        frame1 = Frame(self)
        frame1.pack()  # 包管理器
        label1 = Label(frame1, text="原始图像:")
        self.canvas1 = Canvas(frame1, width=256, height=256, background="white")
        label2 = Label(frame1, text="合成图像:")
        self.canvas2 = Canvas(frame1, width=256, height=256, background="white")
        label3 = Label(frame1, text="水印图像:") #增加一个画布标签
        self.canvas3 = Canvas(frame1, width=256, height=256, background="white")#增加一个显示图像的画布

        label1.grid(row=0, column=0)
        label2.grid(row=0, column=1)
        label3.grid(row=0, column=2) #增加一个画布标签
        self.canvas1.grid(row=1, column=0)
        self.canvas2.grid(row=1, column=1)
        self.canvas3.grid(row=1, column=2) #增加一个显示图像的画布

        frame2 = Frame(self)
        frame2.pack()
        #frame2.height = 8
        #frame2.grid_propagate(0)
        label_src = Label(frame2, text="原图像:")
        self.path = StringVar()
        entry_src = Entry(frame2, textvariable=self.path, state='readonly',width = 4)
        label_mark = Label(frame2, text="水印日期:")
        self.mark = StringVar()
        entry_mark = Entry(frame2, textvariable=self.mark,width = 5)
        entry_mark.insert(0,'12\\23')

        label_pos_x = Label(frame2, text="pos_x:",width = 4)
        self.pos_x = StringVar()
        entry_pos_x = Entry(frame2, textvariable=self.pos_x, width=4)
        entry_pos_x.insert(0, '240')
        label_pos_y = Label(frame2, text="pos_y:",width = 4)
        self.pos_y = StringVar()
        entry_pos_y = Entry(frame2, textvariable=self.pos_y, width=4)
        entry_pos_y.insert(0, '280')

        label_angle = Label(frame2, text="angle:",width = 4)
        self.angle = StringVar()
        entry_angle = Entry(frame2, textvariable=self.angle, width=4)
        entry_angle.insert(0, '110')

        self.list_txt = StringVar()
        scrb_mouse = Scrollbar(frame2)
        #scrb_mouse.pack(side=RIGHT,fill=Y)
        label_mouse = Label(frame2, text='mouse_xy')
        list_press = Listbox(frame2,listvariable = self.list_txt,selectmode = SINGLE,height = 2,width=15)
        #list_press['yscrollcommand'] = scrb_mouse.set
        list_press.insert(END,'1.Transparent','2.Multiply','3.Color_burn','4.Color_dodge','5.Linear_burn')
        list_press.insert(END, '6.Linear_dodge','7.Lighten','8.Dark', '9.Screen', '10.Overlay', '11.Soft_light')
        list_press.insert(END,'12.Hard_light','13.Vivid_light','14.Pin_light','18.Linear_light','19.Hard_light')

        label_src.grid(row=1, column=0)
        entry_src.grid(row=1, column=1)

        label_mark.grid(row=1, column=2)
        entry_mark.grid(row=1, column=3)

        label_pos_x.grid(row=0, column=0)
        entry_pos_x.grid(row=0, column=1)
        label_pos_y.grid(row=0, column=2)
        entry_pos_y.grid(row=0, column=3)
        label_angle.grid(row=0, column=4)
        entry_angle.grid(row=0, column=5)



        label_mouse.grid(row=1, column=4)
        list_press.grid(row = 1 ,column = 5)
        scrb_mouse.grid(row = 1 ,column = 6)


        frame3 = Frame(self)
        frame3.pack()
        btOpenImage = Button(frame3, text="打开图片", command=self.openImage1)
        btOpenImage.grid(columnspan=3, sticky=W, padx=5, pady=3)
        btOpenImage2 = Button(frame3, text="打开水印", command=self.openImage2)
        btOpenImage2.grid(columnspan=12, sticky=W, padx=5, pady=3)

        btProcess = Button(frame3, text="处理", command=self.processButton)
        btProcess.grid(row=0, column=3, columnspan=3, padx=5, sticky=E)

        self.btMore = Button(frame3, text="继续添加水印", state=DISABLED, command=self.markMore)
        self.btMore.grid(row=0, column=6, columnspan=3)

        self.btSave = Button(frame3, text="保存结果", state=DISABLED, command=self.saveImage)
        self.btSave.grid(row=1, column=6, columnspan=3)


    '''# bt1_move = Button(scrb_mouse
           self.canvas1.bind('<B1-Motion>', MouseMove)

    def MouseMove(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        #print(event.x)
        self.label_mouse.text = StringVar(self.mouse_x)'''

    def openImage1(self):  #打开原图像
        #filename = filedialog.askopenfilename(initialdir='E:/',
        #                                      filetypes=[("图像", ".jpg .png .tif")], title='打开')  # 文件打开对话框
        filename = 'image/28.jpg'
        self.srcfile = filename
        self.path.set(filename)
        self.srcImageId = None
        if filename:
            self.srcImage = Image.open(filename).convert(IM_MOD)
            self.tk_srcIm = ImageTk.PhotoImage(self.srcImage.resize((256, 256)))
            if self.srcImageId:
                self.canvas1.delete(self.srcImageId)
                self.srcImageId = None
            self.srcImageId = self.canvas1.create_image(0, 0, anchor=NW, image=self.tk_srcIm)

    def openImage2(self):  #打开水印图像
            #filename = filedialog.askopenfilename(initialdir='E:/',
            #                                     filetypes=[("图像", ".jpg .png .tif")], title='打开')  # 文件打开对话框
            filename = 'image/31.jpg'
            self.markfile = filename
            self.path.set(filename)
            self.markImageId = None
            if filename:
                self.markImage = Image.open(filename).convert(IM_MOD)
                self.tk_markIm = ImageTk.PhotoImage(self.markImage.resize((256, 256)))
                if self.markImageId:
                    self.canvas1.delete(self.markImageId)
                    self.markImageId = None
                self.markImageId = self.canvas3.create_image(0, 0, anchor=NW, image=self.tk_markIm) #将图像显示在新增画布中

    def processButton(self):  #处理水印图像1
        if self.srcImage:
            mark = self.mark.get()
            pos1 = int(self.pos_x.get())
            pos2 = int(self.pos_y.get())
            pos = (int(self.pos_x.get()),int(self.pos_y.get()))
            angled = int(self.angle.get())
            #print pos,angled

            self.dstImageId = None
            if mark and len(mark)>1: #( len(mark) = 2 or len(mark)=4 or (len(mark)=5 and mark[3]='\\'))
                mark = mark.replace('\\', "32",1)
                #self.dstImage =watermark(mark, self.markImage, image=self.srcImage)  # 加水印
                self.dstImage =watermark(mark, mark_pos=pos,angle=angled,path=self.markfile,image=self.srcImage)
                self.tk_dstIm = ImageTk.PhotoImage(self.dstImage.resize((256, 256)))
                if self.dstImageId:
                    self.canvas2.delete(self.dstImageId)
                    self.dstImageId = None
                self.dstImageId = self.canvas2.create_image(0, 0, anchor=NW, image=self.tk_dstIm)
                self.btSave.config(state=NORMAL)  # 激活保存按钮
                self.btMore.config(state=NORMAL)
            else:
                messagebox.showinfo('Error', "未输入日期！请输入水印日期")
        else:
            messagebox.showinfo('Error', "输入图像错误")

    '''def processButton2(self):   #处理水印图像2
        if self.srcImage:
            self.dstImageId = None

            self.dstImage =watermark2( self.srcfile,self.markfile, position =(50,50))  # 加水印
            self.tk_dstIm = ImageTk.PhotoImage(self.dstImage.resize((256, 256)))
            if self.dstImageId:
                self.canvas2.delete(self.dstImageId)
                self.dstImageId = None
            self.dstImageId = self.canvas2.create_image(0, 0, anchor=NW, image=self.tk_dstIm)
            self.btSave.config(state=NORMAL)  # 激活保存按钮
        else:
            messagebox.showinfo('Error', "输入图像错误")
'''
    def saveImage(self): #保存图像
        filename = filedialog.asksaveasfilename(initialdir='E:/', defaultextension='png', title='保存')  # 文件保存对话框
        if filename:
            if self.dstImage:
                self.dstImage.save(filename)
        self.btSave.config(state=DISABLED)

    def markMore(self):  # 继续添加水印图像
        #add shift code
        if self.srcImageId:
            self.canvas1.delete(self.srcImageId)
            self.srcImageId = None
        self.srcImage = self.dstImage
        self.tk_srcIm = ImageTk.PhotoImage(self.srcImage.resize((256, 256)))
        self.srcImageId = self.canvas1.create_image(0, 0, anchor=NW, image=self.tk_srcIm)
        self.btMore.config(state=DISABLED)

#--------------------------------------------------------------------------------
#主程序
root = Tk()
root.resizable(0, 0)
app = watermark_App(root)
app.master.title('水印库测试')

app.mainloop()
