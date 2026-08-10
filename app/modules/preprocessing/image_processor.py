import cv2


class ImageProcessor:
    """
    Performs image enhancement before OCR.
    """

    @staticmethod
    def preprocess(image_path: str):

        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        cv2.imwrite(image_path, thresh)

        return image_path