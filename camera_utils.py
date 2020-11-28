import cv2 as cv
from threading import Thread


class CameraThread(Thread):
    ip_of_camera = '192.168.0.5'
    cap = cv.VideoCapture(f'http://{ip_of_camera}/live')
    image_from_camera_with_didcated_lines = cv.imread('correct_field_with_didicated_lines.png')
    iwdl_in_hsv_csp = cv.cvtColor(image_from_camera_with_didcated_lines, cv.COLOR_BGR2HSV)
    images_of_lines_with_hsv_filter = cv.inRange(iwdl_in_hsv_csp, (0, 0, 0), (255, 200, 255))

    hsv_range_of_markers = {'red': ((147, 53, 147), (255, 255, 255)),
                            'green': ((59, 90, 132), (98, 198, 255)),
                            'blue': ((108, 79, 82), (118, 255, 180))}

    def __init__(self):
        self.image_from_camera = self.cap.read()
        self.current_im_in_hsv_csp = cv.cvtColor(self.image_from_camera, cv.COLOR_BGR2HSV)
        self.images_with_hsv_filter = {}
        self.images_with_morphology_closing = {}
        self.contours_of_markers = {}
        self.centers_of_markers = {}
        self.coordinates_of_lines = {0: (), 1: ()}
        self.error_of_position_from_lines = 0
        self.running = True

    @staticmethod
    def morphology_filter(image):
        edged = cv.Canny(image)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
        closed = cv.morphologyEx(edged, cv.MORPH_RECT, kernel)
        return closed

    def update_markers(self):
        for marker in self.hsv_range_of_markers:
            self.images_with_hsv_filter[marker] = \
                cv.inRange(self.current_im_in_hsv_csp,
                           self.hsv_range_of_markers[marker][0],
                           self.hsv_range_of_markers[marker][1])
            self.images_with_morphology_closing[marker] = \
                self.morphology_filter(self.images_with_hsv_filter)
            self.contours_of_markers[marker] = \
                cv.findContours(self.images_with_morphology_closing[marker].copy(),
                                cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[0]

            for contour in self.contours_of_markers[marker]:
                perimeter = cv.arcLength(contour, True)
                approx_dp = cv.approxPolyDP(contour, 0.1 * perimeter, True)

                if len(approx_dp) == 4 and perimeter > 50:
                    area_of_marker = cv.minAreaRect(approx_dp)
                    self.centers_of_markers[marker] = \
                        (int(area_of_marker[0][0]), int(area_of_marker[0][1]))
                    cv.drawContours(self.image_from_camera_with_didcated_lines,
                                    [approx_dp],
                                    -1,
                                    (0, 255, 0),
                                    4)
                    cv.circle(self.image_from_camera_with_didcated_lines,
                              self.centers_of_markers[marker],
                              3,
                              (0, 255, 255),
                              2)

    def update_coordinates_of_lines_for_following(self):
        image_of_roi_on_image_of_lines = \
            self.images_of_lines_with_hsv_filter[
            int(self.centers_of_markers['red'][1]):int(self.centers_of_markers['blue'][1]),
            int(self.centers_of_markers['red'][0]):int(self.centers_of_markers['blue'][0])
            ]
        image_of_roi_with_morphology_closing = self.morphology_filter(image_of_roi_on_image_of_lines)
        contours_of_lines_on_roi = cv.findContours(image_of_roi_with_morphology_closing.copy(),
                                                   cv.RETR_EXTERNAL,
                                                   cv.CHAIN_APPROX_SIMPLE)[0]
        number_of_coordinate = 0
        for contour in contours_of_lines_on_roi:
            perimeter = cv.arcLength(contour, True)
            approx_dp = cv.approxPolyDP(contour, 0.1 * perimeter, True)
            if len(approx_dp) == 2:
                temp_coordinates = (
                    (approx_dp.item(0) + int(self.centers_of_markers['red'][0]),
                     approx_dp.item(1) + int(self.centers_of_markers['red'][1])),
                    (approx_dp.item(2) + int(self.centers_of_markers['red'][0]),
                     approx_dp.item(3) + int(self.centers_of_markers['red'][1]))
                )
                self.coordinates_of_lines[number_of_coordinate] = temp_coordinates
                cv.line(self.image_from_camera_with_didcated_lines,
                        temp_coordinates[0],
                        temp_coordinates[1],
                        (0, 255, 255),
                        5)
                number_of_coordinate += 1

    def update_error(self):
        if self.centers_of_markers['green'][1] not in range(self.coordinates_of_lines[1][1][1],
                                                            self.coordinates_of_lines[0][1][1]):
            if self.centers_of_markers['green'][1] <= self.coordinates_of_lines[1][1][1]:
                self.error = self.centers_of_markers['green'][1] - self.coordinates_of_lines[1][1][1]
            elif self.centers_of_markers['green'][1] >= self.coordinates_of_lines[0][1][1]:
                self.error = self.centers_of_markers['green'][1] - self.coordinates_of_lines[0][1][1]

    def run(self):
        while self.running:
            retval, self.image_from_camera = self.cap.read()
            self.image_from_camera_with_didcated_lines = cv.imread('correct_field_with_didicated_lines.png')
            if retval:
                self.current_im_in_hsv_csp = cv.cvtColor(self.image_from_camera, cv.COLOR_BGR2HSV)
                self.update_markers()
                self.update_coordinates_of_lines_for_following()
            else:
                print('Check ip address of camera.')
                break
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            cv.imshow('Result', self.image_from_camera_with_didcated_lines)
        self.cap.release()
        cv.destroyAllWindows()