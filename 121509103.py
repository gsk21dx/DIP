import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfilename

file_path = os.path.dirname(__file__)

class ImageSystem:
    def __init__(self):
        self.image = None
        self.gsk = tk.Tk()
        self.gsk.geometry('1200x700+100+100')
        self.gsk.title('图像处理')
        self.gsk.resizable(True, True)
        menubar = tk.Menu(self.gsk)
        self.gsk.config(menu=menubar)

        self.create_menu(menubar, "文件", [
            ("打开", self.open_file),
            ("保存", self.save_file),
            ("复原", self.recover_file),
            ("清除", self.clear_file),
            ("退出", self.exit_system),
        ])

        self.create_menu(menubar, "翻转", [
            ("水平", self.flip_horizontal),
            ("垂直", self.flip_vertical),
            ("水平&垂直", self.flip_hor_ver),
        ])

        self.create_menu(menubar, "形态学", [
            ("腐蚀", self.mor_corrosion),
            ("膨胀", self.mor_expand),
            ("开运算", self.mor_open_operation),
            ("闭运算", self.mor_close_operation),
            ("形态学梯度", self.mor_gradient),
            ("顶帽运算", self.mor_top_hat),
            ("黑帽运算", self.mor_black_hat),
        ])

        self.create_menu(menubar, "滤波", [
            ("均值滤波", self.filter_mean),
            ("方框滤波", self.filter_box),
            ("高斯滤波", self.filter_gauss),
            ("中值滤波", self.filter_mid_value),
            ("双边滤波", self.filter_bilateral),
            ("直方图增强", self.corrected_hist),
        ])

        self.create_menu(menubar, "缩放", [
            ("放大PyrUp", self.scale_pyr_up),
            ("缩小PyrDown", self.scale_pyr_down),
            ("放大Resize", self.scale_zoom_in),
            ("缩小Resize", self.scale_zoom_out),
        ])

        self.create_menu(menubar, "旋转", [
            ("平移", self.rotate_offset),
            ("仿射", self.rotate_affine),
            ("透射", self.rotate_transmission),
            ("顺时针-无缩放", self.rotate_clockwise),
            ("顺时针-缩放", self.rotate_clockwise_zoom),
            ("逆时针-缩放", self.rotate_anti_zoom),
            ("零旋转-缩放", self.rotate_zero_zoom),
        ])

        self.create_menu(menubar, "帮助", [
            ("版权", self.help_copyright),
            ("关于", self.help_about),
        ])

        self.frame_source = ttk.LabelFrame(self.gsk)
        self.frame_source.place(x=60, y=80, width=500, height=500)

        self.frame_destination = ttk.LabelFrame(self.gsk)
        self.frame_destination.place(x=640, y=80, width=500, height=500)

        self.label_source = ttk.Label(self.gsk, text='源图像', font=100, foreground='blue', anchor='center')
        self.label_source.place(x=250, y=30, width=100, height=50)

        self.label_destination = ttk.Label(self.gsk, text='目标图像', font=100, foreground='blue', anchor='center')
        self.label_destination.place(x=860, y=30, width=100, height=50)

        self.label_source_image = None
        self.label_des_image = None
        self.path = ''
        self.gsk.mainloop()

    @staticmethod
    def create_menu(menubar, label, commands):
        menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=label, menu=menu)
        for name, command in commands:
            menu.add_command(label=name, command=command)

    def open_file(self):
        try:
            open_img_path = askopenfilename(initialdir=file_path,
                                            filetypes=[("jpg格式", "jpg"), ("png格式", "png"), ("bmp格式", "bmp")],
                                            parent=self.gsk,
                                            title='打开自定义图片')
            if open_img_path == '':
                return

            if self.label_des_image is not None:
                self.label_des_image.pack_forget()
                self.label_des_image = None

            self.path = open_img_path
            image = Image.open(self.path)
            tk_image = ImageTk.PhotoImage(image)

            if self.label_source_image is None:
                self.label_source_image = tk.Label(self.frame_source, image=tk_image)
                self.label_source_image.configure(image=tk_image)
                self.label_source_image.pack()

            self.gsk.mainloop()

        except Exception as e:
            messagebox.showerror("错误", f"打开文件时出错：{e}")

    def save_file(self):
        try:
            
            save_img_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG格式", "*.png"), ("JPEG格式", "*.jpg"),
                                                                    ("BMP格式", "*.bmp")],
                                                         initialdir=self.path,
                                                         parent=self.gsk,
                                                         title='保存图片')

            if save_img_path == '':
                return

            # 保存图像到指定路径
            self.image.save(save_img_path)

        except Exception as e:
            messagebox.showerror("错误", f"保存文件时出错：{e}")

    def recover_file(self):
        if self.path == '':
            return
        image = Image.open(self.path)
        tk_image = ImageTk.PhotoImage(image)
        if self.label_des_image is None:
            return
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    def clear_file(self):
        if self.label_source_image is not None:
            self.label_source_image.pack_forget()  # 隐藏控件
            self.label_source_image = None
            self.path = ''
        if self.label_des_image is not None:
            self.label_des_image.pack_forget()  # 隐藏控件
            self.label_des_image = None
            self.path = ''

    def exit_system(self):
        quit_gsk = messagebox.askokcancel('提示：', '再次确认退出')
        if quit_gsk:
            self.gsk.destroy()
        return

    def flip_horizontal(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # Flipped Horizontally 水平翻转
        image_hor_flip = cv2.flip(image, 1)
        image_pil_hor_flip = Image.fromarray(image_hor_flip)
        tk_image = ImageTk.PhotoImage(image_pil_hor_flip)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    def flip_vertical(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # Flipped Horizontally 水平翻转
        image_hor_flip = cv2.flip(image, 0)  # 垂直翻转
        image_pil_hor_flip = Image.fromarray(image_hor_flip)
        tk_image = ImageTk.PhotoImage(image_pil_hor_flip)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    def flip_hor_ver(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # Flipped Horizontally 水平翻转
        image_hor_flip = cv2.flip(image, -1)  # 水平垂直翻转
        image_pil_hor_flip = Image.fromarray(image_hor_flip)
        tk_image = ImageTk.PhotoImage(image_pil_hor_flip)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    def mor_corrosion(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_erosion = cv2.erode(image, kernel)  # 腐蚀
        image_pil_erosion = Image.fromarray(img_erosion)
        tk_image = ImageTk.PhotoImage(image_pil_erosion)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()
        # 膨胀

    def mor_expand(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_dilation = cv2.dilate(image, kernel)  # 膨胀
        image_pil_dilation = Image.fromarray(img_dilation)
        tk_image = ImageTk.PhotoImage(image_pil_dilation)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()
        # 开运算

    def mor_open_operation(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_open_operation = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)  # 开运算
        image_pil_open = Image.fromarray(img_open_operation)
        tk_image = ImageTk.PhotoImage(image_pil_open)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()
        # 闭运算

    def mor_close_operation(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_close_operation = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)  # 闭运算
        image_pil_close = Image.fromarray(img_close_operation)
        tk_image = ImageTk.PhotoImage(image_pil_close)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 形态学梯度：膨胀图减去腐蚀图，dilation - erosion，这样会得到物体的轮廓：
    def mor_gradient(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)  # 形态学梯度
        image_pil_gradient = Image.fromarray(img_gradient)
        tk_image = ImageTk.PhotoImage(image_pil_gradient)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 顶帽
    def mor_top_hat(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        kernel = np.ones((7, 7), np.uint8)  # 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_top_hat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)  # 顶帽
        image_pil_top_hat = Image.fromarray(img_top_hat)
        tk_image = ImageTk.PhotoImage(image_pil_top_hat)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 黑帽
    def mor_black_hat(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        kernel = np.ones((7, 7), np.uint8)  # 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构
        img_black_hat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)  # 黑帽
        image_pil_black_hat = Image.fromarray(img_black_hat)
        tk_image = ImageTk.PhotoImage(image_pil_black_hat)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    '''
    常见噪声有椒盐噪声和高斯噪声，椒盐噪声可以理解为斑点，随机出现在图像中的黑点或白点；
    高斯噪声可以理解为拍摄图片时由于光照等原因造成的噪声；这样解释并不准确，只要能简单分辨即可。
    '''

    # 均值滤波
    def filter_mean(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_mean = cv2.blur(image, (3, 3))  # 均值滤波
        image_pil_mean = Image.fromarray(img_mean)
        tk_image = ImageTk.PhotoImage(image_pil_mean)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

        # 方框滤波方框滤波跟均值滤波很像，当可选参数normalize为True的时候，方框滤波就是均值滤波，

    # 如3×3的核，a就等于1/9；normalize为False的时候，a=1，相当于求区域内的像素和。
    def filter_box(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_box = cv2.boxFilter(image, -1, (3, 3), normalize=False)  # 方框滤波
        image_pil_box = Image.fromarray(img_box)
        tk_image = ImageTk.PhotoImage(image_pil_box)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 高斯滤波与两种滤波方式，卷积核内的每个值都一样，相当于图像区域中每个像素的权重也就一样。
    # 高斯滤波的卷积核权重并不相同，中间像素点权重最高，越远离中心的像素权重越小。
    # 高斯滤波相比均值滤波效率要慢，但可以有效消除高斯噪声，能保留更多的图像细节，所以经常被称为最有用的滤波器。
    def filter_gauss(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_gauss = cv2.GaussianBlur(image, (1, 1), 1)  # 方框滤波
        image_pil_gauss = Image.fromarray(img_gauss)
        tk_image = ImageTk.PhotoImage(image_pil_gauss)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 中值滤波，中值又叫中位数，是所有值排序后取中间的值。
    # 中值滤波就是用区域内的中值来代替本像素值，所以那种孤立的斑点，
    # 如0或255很容易消除掉，适用于去除椒盐噪声和斑点噪声。中值是一种非线性操作，效率相比前面几种线性滤波要慢。
    # 斑点噪声图，用中值滤波显然更好：
    def filter_mid_value(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_mid_value = cv2.medianBlur(image, 5)  # 中值滤波
        image_pil_mid_value = Image.fromarray(img_mid_value)
        tk_image = ImageTk.PhotoImage(image_pil_mid_value)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 双边滤波，模糊操作基本都会损失掉图像细节信息，尤其前面介绍的线性滤波器，图像的边缘信息很难保留下来。
    # 然而，边缘edge信息是图像中很重要的一个特征，所以这才有了双边滤波。
    def filter_bilateral(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_bilateral = cv2.bilateralFilter(image, 9, 75, 75)  # 双边滤波
        image_pil_bilateral = Image.fromarray(img_bilateral)
        tk_image = ImageTk.PhotoImage(image_pil_bilateral)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 图像金字塔操作的将是图像的像素问题（图像变清晰了还是模糊了）
    # 图像金字塔主要有两类：高斯金字塔和拉普拉斯金字塔。
    def scale_pyr_up(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_pyr_up = cv2.pyrUp(image)  # 高斯金字塔
        image_pil_pyr_up = Image.fromarray(img_pyr_up)
        tk_image = ImageTk.PhotoImage(image_pil_pyr_up)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    def scale_pyr_down(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        img_pyr_down = cv2.pyrDown(image)  # 高斯金字塔
        image_pil_pyr_down = Image.fromarray(img_pyr_down)
        tk_image = ImageTk.PhotoImage(image_pil_pyr_down)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(rel_x=0,r_ely=0)# 放置组件的不同方式
        self.label_des_image.pack()
        self.gsk.mainloop()

    def corrected_hist(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        r, g, b = cv2.split(image)  # 分离通道
        r1 = cv2.equalizeHist(r)
        g1 = cv2.equalizeHist(g)
        b1 = cv2.equalizeHist(b)
        image_equal_clo = cv2.merge([r1, g1, b1])  # 合并通道

        image_pil_equal_clo = Image.fromarray(image_equal_clo)
        tk_image = ImageTk.PhotoImage(image_pil_equal_clo)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 放大
    def scale_zoom_in(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        size = (2 * image.shape[1], 2 * image.shape[0])
        img_zoom_in = cv2.resize(image, size)  # 放大
        image_pil_zoom_in = Image.fromarray(img_zoom_in)
        tk_image = ImageTk.PhotoImage(image_pil_zoom_in)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.place(x=0, y=0)  # 放置组件的不同方式与金字塔放大相比对齐方式不同显示不同
        # self.label_des_image.pack()
        self.gsk.mainloop()

    # 缩小
    def scale_zoom_out(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        size = (int(0.3 * image.shape[1]), int(0.3 * image.shape[0]))
        img_zoom_out = cv2.resize(image, size)  # 放大
        image_pil_zoom_out = Image.fromarray(img_zoom_out)
        tk_image = ImageTk.PhotoImage(image_pil_zoom_out)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 平移
    def rotate_offset(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        width, height = image.shape[1], image.shape[0]
        direction = np.float32([[1, 0, 50], [0, 1, 50]])  # 沿x轴移动50，沿y轴移动50
        img_offset = cv2.warpAffine(image, direction, (width, height))
        image_pil_offset = Image.fromarray(img_offset)
        tk_image = ImageTk.PhotoImage(image_pil_offset)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 仿射-需要三个点坐标
    def rotate_affine(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        width, height = image.shape[1], image.shape[0]
        pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
        pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
        rot_mat = cv2.getAffineTransform(pts1, pts2)  # 沿x轴移动50，沿y轴移动50
        img_affine = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_affine = Image.fromarray(img_affine)
        tk_image = ImageTk.PhotoImage(image_pil_affine)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 透射 -需要四个点的坐标
    def rotate_transmission(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        _, height = image.shape[1], image.shape[0]
        pts1 = np.float32([[56, 65], [238, 52], [28, 237], [239, 240]])
        pts2 = np.float32([[0, 0], [250, 0], [0, 250], [250, 250]])
        rot_mat = cv2.getPerspectiveTransform(pts1, pts2)
        img_clockwise = cv2.warpPerspective(image, rot_mat, (250, 250))  # 透射与仿射的函数不一样
        image_pil_clockwise = Image.fromarray(img_clockwise)
        tk_image = ImageTk.PhotoImage(image_pil_clockwise)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 顺时针无缩放
    def rotate_clockwise(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width // 2, height // 2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle=-45, scale=1)  # 旋转中心rotate_center，角度degree， 缩放scale
        img_clockwise = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_clockwise = Image.fromarray(img_clockwise)
        tk_image = ImageTk.PhotoImage(image_pil_clockwise)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 顺时针-缩放
    def rotate_clockwise_zoom(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width // 2, height // 2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle=-45, scale=0.6)  # 旋转中心rotate_center，角度degree， 缩放scale
        img_clockwise_zoom = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_clockwise_zoom = Image.fromarray(img_clockwise_zoom)
        tk_image = ImageTk.PhotoImage(image_pil_clockwise_zoom)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 逆时针-缩放
    def rotate_anti_zoom(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width // 2, height // 2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle=45, scale=0.6)  # 旋转中心rotate_center，角度degree， 缩放scale
        img_clockwise_zoom = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_clockwise_zoom = Image.fromarray(img_clockwise_zoom)
        tk_image = ImageTk.PhotoImage(image_pil_clockwise_zoom)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    # 零旋转-缩放
    def rotate_zero_zoom(self):
        if self.path == '':
            return
        if self.label_source_image is None:
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        width, height = image.shape[1], image.shape[0]
        rotate_center = (width // 2, height // 2)
        rot_mat = cv2.getRotationMatrix2D(rotate_center, angle=0, scale=0.6)  # 旋转中心rotate_center，角度degree， 缩放scale
        img_zero_zoom = cv2.warpAffine(image, rot_mat, (width, height))
        image_pil_zero_zoom = Image.fromarray(img_zero_zoom)
        tk_image = ImageTk.PhotoImage(image_pil_zero_zoom)
        if self.label_des_image is None:
            self.label_des_image = tk.Label(self.frame_destination, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(x=0, y=0)
        self.label_des_image.pack()
        self.gsk.mainloop()

    @staticmethod
    def help_copyright():
        tk.messagebox.showinfo(title='版权', message='121509103！')  # 版权属于学号

    @staticmethod
    def help_about():
        tk.messagebox.showinfo(title='关于', message='')


if __name__ == '__main__':
    ImageSystem()
