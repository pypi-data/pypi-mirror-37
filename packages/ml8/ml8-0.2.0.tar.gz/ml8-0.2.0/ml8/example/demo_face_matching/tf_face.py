"""
demo

"""

import os
import logging as log
import numpy as np
import tensorflow as tf
import cv2
import tf_face_conv as myconv

def createdir(*args):
    """
    创建目录
    :param args: 目录名字
    :return:
    """
    for item in args:
        if not os.path.exists(item):
            os.makedirs(item)


IMGSIZE = 64


def getpaddingSize(shape):
    """
    获得使图像成为方形矩形的大小
    :param shape: 维度，例如shape=28，则图片被整理成28x28
    :return:
    """
    h, w = shape
    longest = max(h, w)
    result = (np.array([longest] * 4, int) - np.array([h, h, w, w], int)) // 2
    return result.tolist()


def dealwithimage(img, h=64, w=64):
    """
    处理图片
    :param img: 图像
    :param h: 图片高度
    :param w: 图片宽度
    :return:
    """
    # img = cv2.imread(imgpath)
    top, bottom, left, right = getpaddingSize(img.shape[0:2])
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    img = cv2.resize(img, (h, w))
    return img

def relight(imgsrc, alpha=1, bias=0):
    """
    改变图片亮度
    线性处理，根据一个公式  y = x * alpha + b
    :param imgsrc: 图片
    :param alpha: 公式中的alpha值
    :param bias: 公式中的b值
    :return:
    """
    '''relight'''
    imgsrc = imgsrc.astype(float)
    imgsrc = imgsrc * alpha + bias
    # 经过线性变换以后还要保证图片的像素值在0-255之间，
    # 如果小于0则置0，如果大于255则置为255
    imgsrc[imgsrc < 0] = 0
    imgsrc[imgsrc > 255] = 255
    imgsrc = imgsrc.astype(np.uint8)
    return imgsrc

def getface(imgpath, outdir):
    """
    从路径中得到人脸
    :param imgpath: 图片路径
    :param outdir: 输出路径
    :return:
    """
    ''' get face from path file'''
    filename = os.path.splitext(os.path.basename(imgpath))[0]
    img = cv2.imread(imgpath)
    # haarcascade_frontalface_default.xml是opencv中的一个特征检测器
    # 文件在opencv中的位置为：./opencv/sources/data/haarcascades
    # 本项目已经将该文件下载到本地，在haarcascades文件夹下
    haar = cv2.CascadeClassifier('haarcascades\haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = haar.detectMultiScale(gray_img, 1.3, 5)
    n = 0
    for f_x, f_y, f_w, f_h in faces:
        n += 1
        face = img[f_y:f_y + f_h, f_x:f_x + f_w]
        # 可能现在不需要调整大小
        # face = cv2.resize(face, (64, 64))
        face = dealwithimage(face, IMGSIZE, IMGSIZE)
        for inx, (alpha, bias) in enumerate([[1, 1], [1, 50], [0.5, 0]]):
            facetemp = relight(face, alpha, bias)
            cv2.imwrite(os.path.join(outdir, '%s_%d_%d.jpg' % (filename, n, inx)), facetemp)


def getfilesinpath(filedir):
    """
    从文件目录中取出所有的文件
    :param filedir: 文件目录
    :return:
    """
    for (path, dirnames, filenames) in os.walk(filedir):
        for filename in filenames:
            if filename.endswith('.jpg'):   # 判断文件是否是以.jpg结尾的
                yield os.path.join(path, filename)
        for diritem in dirnames:
            getfilesinpath(os.path.join(path, diritem))


def generateface(pairdirs):
    """
    生成人脸
    :param pairdirs: 图像的输入路径和输出路径
    :return:
    """
    for inputdir, outputdir in pairdirs:
        for name in os.listdir(inputdir):
            inputname, outputname = os.path.join(inputdir, name), os.path.join(outputdir, name)
            if os.path.isdir(inputname):
                createdir(outputname)
                for fileitem in getfilesinpath(inputname):
                    getface(fileitem, outputname)


def readimage(pairpathlabel):
    """
    读取数据集下的所有文件，数据集中的每个数据都是一个文件夹，以姓名命名
    :param pairpathlabel: 一个数据集的路径
    :return:返回数据集的数据(图片)以及相对应的标签(姓名)
    """
    imgs = []
    labels = []
    for filepath, label in pairpathlabel:
        for fileitem in getfilesinpath(filepath):
            img = cv2.imread(fileitem)
            imgs.append(img)
            labels.append(label)
    return np.array(imgs), np.array(labels)


def onehot(numlist):
    """
    得到一个矩阵序号
    把姓名转换成数字，例如有zonas，wangzongchao两个姓名，则分别转换成0和1
    :param numlist:姓名的列表
    :return:
    """
    ''' get one hot return host matrix is len * max+1 demensions'''
    b = np.zeros([len(numlist), max(numlist) + 1])
    b[np.arange(len(numlist)), numlist] = 1
    return b.tolist()


def getfileandlabel(filedir):
    """
    将人脸从子目录内读出来，根据不同的人名，分配不同的onehot值，这里是按照遍历的顺序分配序号，然后训练，完成之后会保存checkpoint
    图像识别之前将像素值转换为0到1的范围
    需要多次训练的话，把checkpoint下面的上次训练结果删除，代码有个判断，有上一次的训练结果，就不会再训练了

    :param filedir:
    :return:
    """
    ''' get path and host paire and class index to name'''
    dictdir = dict([[name, os.path.join(filedir, name)] \
                    for name in os.listdir(filedir) if os.path.isdir(os.path.join(filedir, name))])
    # for (path, dirnames, _) in os.walk(filedir) for dirname in dirnames])

    dirnamelist, dirpathlist = dictdir.keys(), dictdir.values()
    indexlist = list(range(len(dirnamelist)))

    return list(zip(dirpathlist, onehot(indexlist))), dict(zip(indexlist, dirnamelist))

def demo_face():
    savepath = './checkpoint/face.ckpt'
    exists_ckpt = False # 判断是否存在模型文件
    if os.path.exists(savepath + '.meta'):
        exists_ckpt = True
    if exists_ckpt:
        testfromcamera(savepath)
    else:
        print (u"找不到模型文件")


def main(_):
    savepath = './checkpoint/face.ckpt'
    exists_ckpt = False # 判断是否存在模型文件
    if os.path.exists(savepath + '.meta'):
        exists_ckpt = True
    if exists_ckpt:
        testfromcamera(savepath)
    else:
        print (u"找不到模型文件")


def testfromcamera(chkpoint):
    """
    识别图像
    从训练的结果中恢复训练识别的参数，然后用于新的识别判断
    打开摄像头，采集到图片之后，进行人脸检测，检测出来之后，进行人脸识别，根据结果对应到人员名字，显示在图片中人脸的上面
    :param chkpoint:
    :return:
    """
    camera = cv2.VideoCapture(0)
    haar = cv2.CascadeClassifier('haarcascades\haarcascade_frontalface_default.xml')
    pathlabelpair, indextoname = getfileandlabel('./image/trainfaces')
    output = myconv.cnnLayer(len(pathlabelpair))
    # predict = tf.equal(tf.argmax(output, 1), tf.argmax(y_data, 1))
    predict = output

    saver = tf.train.Saver()
    with tf.Session() as sess:
        # sess.run(tf.global_variables_initializer())
        saver.restore(sess, chkpoint)

        n = 1
        while 1:
            if (n <= 20000):
                print('It`s processing %s image.' % n)
                # 读帧
                success, img = camera.read()

                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = haar.detectMultiScale(gray_img, 1.3, 5)
                for f_x, f_y, f_w, f_h in faces:
                    face = img[f_y:f_y + f_h, f_x:f_x + f_w]
                    face = cv2.resize(face, (IMGSIZE, IMGSIZE))
                    # could deal with face to train
                    test_x = np.array([face])
                    test_x = test_x.astype(np.float32) / 255.0

                    res = sess.run([predict, tf.argmax(output, 1)],
                                   feed_dict={myconv.x_data: test_x,
                                              myconv.keep_prob_5: 1.0, myconv.keep_prob_75: 1.0})
                    print(res)

                    cv2.putText(img, indextoname[res[1][0]], (f_x, f_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)  # 显示名字
                    img = cv2.rectangle(img, (f_x, f_y), (f_x + f_w, f_y + f_h), (255, 0, 0), 2)
                    n += 1
                cv2.imshow('img', img)
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    break
            else:
                break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(0)

