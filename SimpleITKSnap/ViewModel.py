from typing import Tuple

import SimpleITK as sitk
import numpy as np
from cv2 import resize
from numpy import ndarray

from SimpleITKSnap.utils.ImageUtils2D import resizeBySpacing
from SimpleITKSnap.utils.ImageUtils3D import normalizeToGrayScale8


class View3D:
    def __init__(self, array: ndarray, displaySize: Tuple[int, int],
                 spacing: Tuple[float, float, float] = (1, 1, 1)) -> None:
        self.data = array
        self.grayScale8 = normalizeToGrayScale8(self.data)
        self.displaySize = displaySize
        self.spacing = spacing

    def getXSlice(self, x: int) -> ndarray:
        return resizeBySpacing(self.grayScale8[x, :, :], self.displaySize, (self.spacing[0], self.spacing[1]))

    def getYSlice(self, y: int) -> ndarray:
        return resizeBySpacing(self.grayScale8[:, y, :], self.displaySize, (self.spacing[0], self.spacing[2]))

    def getZSlice(self, z: int) -> ndarray:
        return resizeBySpacing(self.grayScale8[:, :, z], self.displaySize, (self.spacing[1], self.spacing[2]))

    def getExtensionInfo(self, extensionFunc, x: int, y: int, z: int) -> (ndarray, str):
        img, s = extensionFunc(self.data, x, y, z)
        return resize(img, self.displaySize), s


class FileView3D(View3D):
    def __init__(self, imgDir: str, displaySize: Tuple[int, int]) -> None:
        sitkImg = sitk.ReadImage(imgDir)
        spacing = sitkImg.GetSpacing()
        array = sitk.GetArrayFromImage(sitkImg)
        array = np.flip(array, 0)
        super().__init__(array, displaySize, spacing)
