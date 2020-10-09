import cv2
import numpy as np

class ImagePreprocessor():
    def Transform(self, image, face_rect):
        # BGR to gray
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Put target pixels to transform image
        transform_image = gray_image[face_rect.top():face_rect.bottom(),
                                     face_rect.left():face_rect.right()]
        transform_image = transform_image / 255

        # Resize to 48 * 48
        transform_image = cv2.resize(transform_image, (48, 48), interpolation=cv2.INTER_CUBIC)

        return transform_image