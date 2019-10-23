# -*- coding: utf-8 -*-
from img_function import *
import time
total = 0
place_succ = 0
svm_0_error = 0
svm_1_error = 0
card = CardPredictor()
time_begin = time.time()
for root, dirs, files in os.walk("test"):
    for filename in files:
        total = total + 1 
        filepath = os.path.join(root, filename)
        src = img_read(filepath)
        img, oldimg = card.img_first_pre(src)
        pre_sobel = card.operator_comp(img, "sobel")
        pre_canny = card.operator_comp(img, "canny")
        predict_result, roi, card_color, standard_part = card.img_only_color(pre_sobel, oldimg)
        if roi is None or roi.size == 0:  # 如果定位失败，换一种定位方式
            predict_result, roi, card_color, standard_part = card.img_color_contours(pre_sobel, oldimg)
        if roi is not None:
            if roi.size:
                # place_succ = place_succ + 1  或许应该考虑识别到三个字符以上才算定位成功
                count = 0
                for i in range(min(len(predict_result), 7)):
                    if predict_result[i] == filename[i]:
                        count = count+1
                if count == 7:
                    svm_0_error = svm_0_error + 1
                    place_succ = place_succ + 1
                elif count == 6:
                    place_succ = place_succ + 1
                    svm_1_error = svm_1_error + 1
                elif count >= 3:
                    place_succ = place_succ + 1
                # cv2.imshow("card img", roi)
                # cv2.waitKey(0)

        print("识别结果：", ''.join(predict_result[:7]), card_color)
        print("文件名", filename[:7])
time_end = time.time()
print("读取的图片总数：", total)
print("定位成功的图片数：", place_succ)
print("定位准确率：", place_succ/total*100)
print("完全预测正确的图片数：", svm_0_error)
print("一个字符错误的图片数：", svm_1_error)
print("识别准确率：", svm_0_error/place_succ*100)
print("耗时：", time_end-time_begin)

"""
root = "C:/Users/iris/Desktop/re"
filename = "川AGQ973no.jpg"
filepath = os.path.join(root, filename)
src = img_read(filepath)
card = CardPredictor()
img, oldimg = card.img_first_pre(src)
pre_sobel = card.operator_comp(img, "sobel")
pre_canny = card.operator_comp(img, "canny")
pre_laplacian = card.operator_comp(img, "laplacian")
# predict_result, roi, card_color, standard_part = card.img_color_contours(pre_sobel, oldimg)
predict_result, roi, card_color, standard_part = card.img_only_color(pre_sobel, oldimg)
print(predict_result[:7], card_color)

if len(standard_part) == 7:
    filepath = ""
    for i in range(7):
        if i == 0:
            root = "C:/Myprogram/Pycharm Projects/new_data/charsChinese"
            province_name = svm_recg.dic[filename[0]]
            filepath = os.path.join(root, province_name)
        else:
            root = "C:/Myprogram/Pycharm Projects/new_data/chars2"
            filepath = os.path.join(root, filename[i])
        print(filepath)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        finalpath = os.path.join(filepath, filename[1:7]+str(i))
        cv2.imwrite(finalpath+".jpg", standard_part[i])
if roi is not None:
    if roi.size:
        cv2.imshow("card img", roi)
        cv2.waitKey(0)
"""


