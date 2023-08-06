import goodlens_ocr_preprocessing.cropper as cropper
import cv2
import numpy as np


class PreProcessing:
    def __init__(self, file_location, width=1800):
        self.image = cv2.imread(file_location)
        self.image_width, self.image_height, _ = self.image.shape
        factor = max(0.5, float(width / self.image_width))
        size = int(factor * self.image_width), int(factor * self.image_height)
        self.image = cv2.resize(self.image, size)

    def cropper(self):
        cropped_image = cropper.process_image(self.image)
        self.image = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)

    def remove_background(self):
        self.image = cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 21)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.bilateralFilter(self.image, 9, 75, 75)
        self.image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)

    def remove_line(self, kernel=(1, 100)):
        kernel_1 = np.ones(kernel, np.uint8)

        morphed = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel_1)
        gray_inv = cv2.bitwise_not(self.image)
        self.image = cv2.bitwise_not(cv2.bitwise_and(gray_inv, morphed))

    def remove_noise(self, kernel=(5, 5)):
        kernel_2 = np.ones(kernel, np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel_2)

    def smooth_text(self, kernel=(5, 5)):
        kernel_2 = np.ones(kernel, np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel_2)

    def get_binary_image(self):
        return self.image

    def to_image_file(self, location):
        cv2.imwrite(location, self.image)
        return True


def pre_processing(src, find_text_area=True, remove_background=True, remove_noise=True, smooth_text=True,
                   to_image=False, output_image_location=None):
    """
        pre_processing(src, find_text_area, remove_background, remove_noise, smooth_text, to_image, output_image_location) -> RGB Array
        .   @param src 원본 이미지 경로
        .   @param find_text_area 글자 영역만 찾아서 분석할지 여부
        .   @param remove_background 배경을 제거하고 글자와 선만 남게 만들지 여부
        .   @param remove_noise 노이즈 제거여부 (빈 공간 영역에서의 의미 없는 점들을 제거한다.)
        .   @param smooth_text 글자 안에 비어있는 점이 있을 경우 영역을 채울지 여부
        .   @param to_image 이미지를 파일로 저장할지 여부
        .   @param output_image_location 파일로 저장할 시, 파일의 저장경로를 설정한다.
        """
    image = PreProcessing(src)
    if find_text_area:
        image.cropper()
    if remove_background:
        image.remove_background()
    if remove_noise:
        image.remove_noise()
    if smooth_text:
        image.smooth_text()

    if to_image:
        if output_image_location is None:
            raise RuntimeError('Set the output image location.')
        return image.to_image_file(output_image_location)
    else:
        return image.get_binary_image()
