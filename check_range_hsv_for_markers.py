hsv_range_of_markers = {'red': ((147, 100, 120), (255, 255, 255)),
                        'green': ((50, 100, 95), (104, 255, 208)),
                        'blue': ((100, 93, 83), (120, 255, 255))}

import cv2 as cv

ip_of_camera = '192.168.0.5'
cap = cv.VideoCapture(f'http://{ip_of_camera}/live')

while True:
    r, i = cap.read()
    for h in hsv_range_of_markers:
        i = cv.cvtColor(i, cv.COLOR_BGR2HSV)
        o = cv.inRange(i, hsv_range_of_markers[h][0], hsv_range_of_markers[h][1])
        o = cv.resize(o, (800, 600))
        cv.imshow(h, o)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()