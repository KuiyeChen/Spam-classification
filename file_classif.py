#将邮件分为垃圾邮件和正常邮件两类

import numpy as np
import os
import shutil

def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

def file_name(file_dir,result):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            str1=os.path.splitext(file)
            if str1[1]=='.eml':
                index1=int(str1[0].split('_')[1])-1
                print(index1)
                if result[index1]==1:
                    mymovefile(file_dir+'/'+file,'ham/'+str1[0].split('_')[1]+str1[1])
                elif result[index1]==0:
                    mymovefile(file_dir+'/'+file, 'spam/'+str1[0].split('_')[1]+str1[1])


def move():
    result = np.loadtxt('spam-mail.tr.label', skiprows=1, delimiter=',', dtype=int, usecols=1)
    file_name('TR',result)