from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

def padd(im, desired_size):
    old_size = im.shape[:2] # old_size is in (height, width) format
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    # new_size should be in (width, height) format
    im = cv2.resize(im, (new_size[1], new_size[0]))
    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)
    color = [255, 255, 255]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,value=color)
    return new_im

def extract_from_image(fileName, size):
    image = cv2.imread(fileName)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    digitCnts = {}
    imgcopy = image.copy()
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        
        if w >= 3 and (h >= 8):
            if y not in digitCnts:
                digitCnts[y] = {}
            digitCnts[y][x] = padd(imgcopy[y:y+h, x:x+w], size)
    return digitCnts


#cv2.imwrite('amtsidebarfind.png', imgcopy)
