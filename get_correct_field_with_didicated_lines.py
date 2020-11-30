import cv2 as cv

ip_of_camera = '192.168.0.5'
cap = cv.VideoCapture(f'http://{ip_of_camera}/live')

hsv_range_of_lines = ((10, 10, 0), (130, 128, 109))

while True:
    retval, image = cap.read()
    i = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    hsvcsp = cv.inRange(image, hsv_range_of_lines[0], hsv_range_of_lines[1])
    edged = cv.Canny(hsvcsp, 1, 25)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    closed = cv.morphologyEx(hsvcsp, cv.MORPH_RECT, kernel)
    cntrs = cv.findContours(closed.copy(),
                                cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[0]
    for contour in cntrs:
        perimeter = cv.arcLength(contour, True)
        approx_dp = cv.approxPolyDP(contour, 0.001 * perimeter, True)

        if perimeter > 1500 and perimeter < 2000:
            cv.drawContours(image,
                           [approx_dp],
                           -1,
                           (255
                            , 0, 0),
                           4)

    cv.imshow('res', image)
    cv.imshow('clsd', closed)
    cv.imshow('hsvcsp', hsvcsp)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.imwrite('img_patterns/correct_field_with_didicated_lines.png', image)
cap.release()
cv.destroyAllWindows()