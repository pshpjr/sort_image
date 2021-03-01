# 해리스 코너 검출 (corner_harris.py)

import cv2
import numpy as np
import os,glob


def compare_img(image_a, image_b):

    kp1, desc1 = image_a
    kp2, desc2 = image_b


    # Flann 매처 생성 ---③
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)
    # knnMatch, k=2 ---③
    matches = matcher.knnMatch(desc1, desc2, 2)




    #첫번재 이웃의 거리가 두 번째 이웃 거리의 75% 이내인 것만 추출---⑤
    ratio = 0.79
    good_matches = [first for first, second in matches \
                    if first.distance < second.distance * ratio]
    return good_matches


os.chdir(r"C:\\")#write file location

fileList = glob.glob(r'*.jpg') + glob.glob(r'*.png')

image_set = [(cv2.resize(cv2.imread(i),(200,200))) for i in fileList]

detector = cv2.ORB_create(scoreType=cv2.ORB_FAST_SCORE,fastThreshold=3,nlevels=1,nfeatures=150)

key_image = [detector.detectAndCompute(i, None) for i in image_set]

zip_image = [[i] for i in zip(fileList, key_image)]

group = [zip_image[0]]

del zip_image[0]

for img_compare in zip_image:
    check = 0

    for img_grouped in group:
        a = compare_img(img_grouped[0][1], img_compare[0][1])
        if len(a)>30 :
            group[group.index(img_grouped)].append(img_compare[0])
            check = 1
            break
    if check == 0:
        group.append(img_compare)

group = sorted(group, key=len, reverse=True)

for i in group:
    for j in i:
        print(j[0])

    print("")

num = 1
for i in group:
    for j in i:
        os.rename(j[0], str(num) + ".jpg")
        num += 1