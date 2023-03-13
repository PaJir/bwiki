# import the necessary packages
# copy from https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
import numpy as np
import imutils
import cv2
# detect template in images
# load the image image, convert it to grayscale, and detect edges
template = cv2.imread("pirates_girl.png")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
# cv2.imshow("Template", template)

def detector(gray, scale, found):
    resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])
    if resized.shape[0] < tH or resized.shape[1] < tW:
        return found
    # detect edges in the resized, grayscale image and apply template matching to find the template in the image
    resized = cv2.Canny(resized, 50, 200)
    result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    # if we have found a new maximum correlation value, then update the bookkeeping variable
    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, r)
    return found

# loop over the images to find the template in
for imagePath in ["panzi_example.jpg"]:
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    for scale in np.linspace(2.0, 1.0, 20)[::-1]:
        found = detector(gray, scale, found)
    if not found:
        continue
    (maxVal, maxLoc, r) = found
    print(maxVal, maxLoc)
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    # draw a bounding box around the detected result and display the image
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", image)
cv2.waitKey(0)
