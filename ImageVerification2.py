# −*− coding: UTF−8 −*−
import time
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage import io,data,color,filters,morphology,transform,draw,measure
from code import *
import datetime
import StringIO
from numpy import array,uint8


class Code_verificat():
    def __init__(self):
        self.imglist = []
        self.dir = './tmp/'
        self.outdir = './out/'
        self.h = 0  # 验证码的高
        self.w = 0  # 验证码的宽

    def get_url(self):
        lt = time.localtime()#UTC格式当前时区时间
        st = time.strftime("%a %b %d %Y %H:%M:%S",lt)
        date =  st + " GMT+0800 (CST)"
        url = "http://www.potalapalace.cn/user/createValidateAction.do?d&%s"%date
        return url

    def del_images(self):
        for f in os.listdir(self.dir):
            os.remove(self.dir+f)

    def request_image_from_path(self,path):
        l = []
        l.append(path + '/*.png')
        l.append(path + '/*.jpg')
        str = ":".join(l)
        coll = io.ImageCollection(str)
        log("读取文件%s"%len(coll))
        for i in coll:
            self.imglist.append(Image.fromarray(uint8(i)))

    def request_image(self):
        """下载图片"""
        data = urllib.urlopen(self.get_url()).read()
        log("结束下载图片")
        return Image.open(StringIO.StringIO(data))

    def down_load_image(self,num):
        for i in range(num):
            log("开始下载: %s"%i)
            self.imglist.append(self.request_image())

    def get_img(self,index):
        img =  self.imglist[index]
        self.w,self.h = img.size
        return img

    def save_image_list(self):
        for f in os.listdir(self.dir):
            os.remove(self.dir+f)
        k = 0
        for i in self.imglist:
            self.save_img(self.dir,i,"%s.jpg"%k)
            k = k + 1
        pass

    def save_img(self,path,img,name):
        img.save(path + name)

    def save_out_img(self,img,name):
        self.save_img(self.outdir,img,name)

    # 二值化
    def binary(self,img):
        img = array(img.convert('L'))
        thresh =filters.threshold_otsu(img)   #返回一个阈值
        #print thresh
        dst =(img <= thresh)*1.0   #根据阈值进行分割
        return dst

    # 膨胀
    def dilation(self,data):
        return morphology.binary_dilation(data, selem=None)

    #先腐蚀再膨胀，可以消除小物体或小斑块。
    #腐蚀（erosion)
    def erosion(self,data):
        return morphology.binary_erosion(data, selem=None)

    # 开运算（opening)
    def openning(self,data):
        return morphology.binary_opening(data,selem=None)

    # 闭运算（closing)
    def closing(self,data):
        return morphology.binary_closing(data,selem=morphology.square(1))

    def bin2img(self,data):
        return Image.fromarray(uint8(data*255))

    def img2bin(self,img):
        return array(img)

    def show_image(self,data,scale=1):
        Image.fromarray(uint8(transform.rescale(data*255, scale))).show()

    # 左上右下
    def crop(self,img,box):
        return img.crop(box)

    # threshold： 阈值，可先项，默认为10
    # line_length: 检测的最短线条长度，默认为50
    #
    # line_gap: 线条间的最大间隙。增大这个值可以合并破碎的线条。默认为10
    #
    # 返回：
    #
    # lines: 线条列表, 格式如((x0, y0), (x1, y0))，标明开始点和结束点。
    def hough_line(self,img,threshold=10, line_length=65,line_gap=3):
        return transform.probabilistic_hough_line(img, threshold=threshold, line_length=line_length,line_gap=line_gap)

    def get_line_points(self,line):
        star = line[0]
        end = line[1]
        return draw.line(star[0],star[1],end[0],end[1])

    def convex_hull_image(self,data):

        chull = morphology.convex_hull_image(data)

        # 将bool数组转成　int
        data = data * 1
        return data

    def remove_small_objects(self,data,min_size=100,connectivity=1):
        # 生成ｂｏｏｌ数组
        data = data == 1
        data = morphology.remove_small_objects(data, min_size=min_size, connectivity=connectivity)
        # 将bool数组转成　int
        data = data * 1

        return data

    # 8连通区域标记
    def label(self, data,connectivity=2):
        labels = measure.label(data, connectivity=2)
        return labels

    # 通过label 获取图片的模板,可以通过coords取的坐标
    def split_label(self,labels,num):
        return measure.regionprops(labels)[num].coords

    # 从data中取的4个文字
    def get_4_char(self,data):
        l = []
        font_t = self.get_font_templete()
        start_point = [(9,3),(21,7),(34,1),(46,5)]
        for i in range(4):
            font = np.zeros(font_t.shape)
            for x in range(font_t.shape[0]):
                for y in range(font_t.shape[1]):
                    if font_t[x,y] == 1:
                        #print data[start_point[1] + x,start_point[0] + y]
                        font[x,y] = data[start_point[i][1] + x,start_point[i][0] + y]
            l.append(font)
        return l
        #l[0] = fill_font

    # 生成文字的大小
    def get_font_templete(self):
        size = (13,13)
        font = np.zeros(size)
        for y in range(13):
            for x in range(13):
                if y < 2 and x > 1:
                    font[y,x] = 1
                elif 2 <= y <7 and 1< x < 11:
                    font[y,x] = 1
                elif 7 <= y < 9 and 1< x < 11:
                    font[y,x] = 1
                elif 9 <= y < 11 and x < 11:
                    font[y,x] = 1
                elif 11 <= y and x < 10:
                    font[y,x] = 1
               # font[y,x] = 1
        return font
        pass

    # 生成签名
    def signature(self,font_data):
        w,h = font_data.shape
        l =[]
        for x in range(w):
            for y in range(h):
                count = 0



    # 删除直线，并且返回删除的点
    def remove_line(self,data):
        left = 5
        right = 63

        # 去四边
        data[:,:2] = 0
        data[:,66:] = 0
        data[:2,:] = 0
        data[21:,:] = 0

        tmp_data = self.erosion(data)
        h = 23

        lefts = []
        while len(lefts) < 1:
            left = left + 1
            lefts = [y for y in range(h) if tmp_data[y,left] == True ]

        rights = []
        while len(rights) < 1:
            right = right - 1
            rights = [y for y in range(h) if tmp_data[y,right]  == True]

        line = []
        step = 1
        if lefts[0] < rights[0]:
            step = 1
        else:
            step = -1

        y_array = range(lefts[0],rights[0] + step,step)
        x_array = range(left,right)

        # 左右均置空
        data[:,:left] = 0
        data[:,right:] = 0

        for y in y_array:
            for x in x_array:

                if tmp_data[y][x + 1] == 1 or tmp_data[y][x] == 1:
                    #print (x,y)
                    line.append((x, y - 1))
                    line.append((x,y))
                    line.append((x, y+1))

                    data[y+1][x] = 0
                    data[y][x] = 0
                    data[y-1][x] = 0
                    x_array = x_array[1:]
                else:
                    break
        return line


if __name__ == '__main__':

    c=Code_verificat()
    total = 300

    # 下载图片
    # c.down_load_image(total)
    # c.save_image_list()

    # 读取图片文件
    c.request_image_from_path(c.dir)

    # 找到图片的切分点v
    img_org = c.get_img(0)
    bins = c.binary(img_org)

    for i in range(1,total):
        img_org = c.get_img(i)
        bin = c.binary(img_org)
        # 去掉直线
        c.remove_line(bin)

        tmp = c.get_4_char(bin)
        for j in range(4):
            c.signature(tmp[j])
            c.save_out_img(c.bin2img(tmp[j]),"%s_%s.jpg"%(i,j))



