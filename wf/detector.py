# import the necessary packages
# from https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
#      http://www.juzicode.com/opencv-python-matchtemplate/
import numpy as np
import imutils
import cv2
import os

MIN_THRESH_BEST = 0.20
MIN_THRESH_MAIN = 0.15
MIN_THRESH_SUB = 0.10
STEP = 90
UNIT_SIZE = 132
SUB_MAIN_RATIO = 82 / 69
DEBUG = True
unit_path = "unit"
equip_path = "equip"
input_path = "input"
out_file = "盘子out.txt"

def detector(template, resized, thresh):
    # detect edges in the resized, grayscale image and apply template matching to find the template in the image
    resized = cv2.Canny(resized, 50, 200)
    result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
    val, result = cv2.threshold(result, thresh, 1.0, cv2.THRESH_BINARY)
    match_locs = cv2.findNonZero(result)
    return match_locs

def getMaxVal(template, plate_gray, scale):
    resized = imutils.resize(plate_gray, width=int(plate_gray.shape[1] * scale))
    resized = cv2.Canny(resized, 50, 200)
    result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(result)
    return max_val

def getBestRatio(templates, plate_gray):
    """templates size: 132x132
    scale plate to fit templates
    width: [templates*6, templates*15]
    """
    (img_height, img_width) = plate_gray.shape[:2]
    (tmp_height, tmp_width) = (UNIT_SIZE, UNIT_SIZE)
    min_scale = tmp_width*6/img_width
    max_scale = tmp_width*15/img_width
    scales = np.linspace(min_scale, max_scale, STEP)
    found = 0
    for template in templates:
        for i in range(STEP//2, STEP, 2):
            if getMaxVal(template, plate_gray, scales[i]) >= MIN_THRESH_BEST or \
                getMaxVal(template, plate_gray, scales[STEP - i]) >= MIN_THRESH_BEST:
                found = i
                break
        if found:
            l = scales[max(0, found-20)] if i <= STEP//2 else scales[found-1]
            r = scales[min(STEP-1, found+20)] if i>= STEP//2 else scales[found+1]
            iters = 10
            while iters:
                iters -= 1
                m1 = (l + r) / 2
                m2 = (m1 + r) / 2
                val1 = getMaxVal(template, plate_gray, m1)
                val2 = getMaxVal(template, plate_gray, m2)
                if val1 < val2:
                    l = m1
                else:
                    r = m2
            return m1
    return None
    
def labelImg(template, plate, ratio, plate_img, thresh):
    match_locs = detector(template, plate, thresh)
    if match_locs is None:
        return None
    locs = [match_locs[0][0]]
    for i in range(1, len(match_locs)):
        if -50 < locs[-1][1] - match_locs[i][0][1] < 50:
            continue
        else:
            locs.append(match_locs[i][0])
    if DEBUG:
        print(locs)
    for loc in locs:
        (startX, startY) = (int(loc[0] * ratio), int(loc[1] * ratio))
        (endX, endY) = (int((loc[0]+UNIT_SIZE)*ratio), int((loc[1]+UNIT_SIZE)*ratio))
        cv2.rectangle(plate_img, (startX, startY), (endX, endY), (0, 0, 255), 2)
    return locs

if __name__ == "__main__":
    for path in [unit_path, equip_path, input_path]:
        if not os.path.exists(path):
            os.makedirs(path)
    units = os.listdir(unit_path)
    units = [os.path.join(unit_path, _) for _ in units]
    units_t = []
    for t in units:
        # template = cv2.imread(t)
        template = cv2.imdecode(np.fromfile(t, dtype=np.uint8), -1)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        units_t.append(template)
    equips = os.listdir(equip_path)
    equips = [os.path.join(equip_path, _) for _ in equips]
    plates = os.listdir(input_path)
    plates = [os.path.join(input_path, _) for _ in plates]
    for plate_path in plates:
        # plate_img = cv2.imread(plate_path)
        plate_img = cv2.imdecode(np.fromfile(plate_path, dtype=np.uint8), -1)
        plate_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        best_ratio = getBestRatio(units_t, plate_gray)
        if not best_ratio:
            if DEBUG:
                print("No units for ", plate_path)
            continue
        plate = imutils.resize(plate_gray, width=int(plate_gray.shape[1] * best_ratio))
        plate = cv2.Canny(plate, 50, 200)
        ratio = plate_gray.shape[1] / float(plate.shape[1])
        plate2 = imutils.resize(plate_gray, width=int(plate_gray.shape[1] * best_ratio * SUB_MAIN_RATIO))
        plate2 = cv2.Canny(plate2, 50, 200)
        ratio2 = plate_gray.shape[1] / float(plate2.shape[1])
        if DEBUG:
            print(plate_path, best_ratio, ratio)
        for template in units_t:
            locs = labelImg(template, plate, ratio, plate_img, MIN_THRESH_MAIN)
            locs = labelImg(template, plate2, ratio2, plate_img, MIN_THRESH_SUB)
        cv2.imshow(plate_path, plate_img)
        cv2.waitKey(0)