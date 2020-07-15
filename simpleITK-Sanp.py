import sys
import numpy as np
from numpy import ndarray
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QDialog,
                             QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget)
from PyQt5.QtGui import QImage, QPixmap


import utils.View3D as View3D


def ndarrayToQPixmap(img: ndarray, fmt=QImage.Format_Grayscale8) -> QPixmap:
    height, width = img.shape[:2]
    pixelSize = 1 if fmt == QImage.Format_Grayscale8 else 3
    qImg = QImage(img.data, width, height,
                  pixelSize*width, fmt)
    return QPixmap(qImg)


class SimpleITKSnap(QDialog):
    def __init__(self, imageFile: str):
        super(SimpleITKSnap, self).__init__()
        # load image
        self.imageData = View3D(imageFile, (300, 300), False)
        self.imageShape = self.imageData.shape

        self.createXViewGroupBox()
        self.createYViewGroupBox()
        self.createZViewGroupBox()
        self.createInfoGroupBox()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.XViewGroupBox, 1, 0)
        mainLayout.addWidget(self.YViewGroupBox, 1, 1)
        mainLayout.addWidget(self.ZViewGroupBox, 2, 0)
        mainLayout.addWidget(self.infoGroupBox, 2, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("Simple-ITKSnap")

    def setX(self, x):
        self.x = x
        # IMAGE
        image = self.imageData.getXSlice(self.x)
        self.imLabelX.setPixmap(ndarrayToQPixmap(image))
        # INDEX
        self.idxLabelX.setText("{}/{}".format(self.x + 1, self.imageShape[0]))

    def setY(self, y):
        self.y = y
        # IMAGE
        image = self.imageData.getYSlice(self.y)
        self.imLabelY.setPixmap(ndarrayToQPixmap(image))
        # INDEX
        self.idxLabelY.setText("{}/{}".format(self.y + 1, self.imageShape[1]))

    def setZ(self, z):
        self.z = z
        # IMAGE
        image = self.imageData.getZSlice(self.z)
        self.imLabelZ.setPixmap(ndarrayToQPixmap(image))
        # INDEX
        self.idxLabelZ.setText("{}/{}".format(self.z + 1, self.imageShape[2]))

    # def createViewGroupBox(self, axis: str, name: str = ""):
    #     self.ViewGroupBox[axis] = QGroupBox(name)

    #     self.imLabel[axis] = QLabel()

    #     slider = QSlider(Qt.Horizontal, self.XViewGroupBox)
    #     slider.setMinimum(0)
    #     slider.setMaximum(self.imageShape[0]-1)
    #     slider.valueChanged.connect(self.setX)
    #     # INDEX
    #     self.idxLabelX = QLabel()

    def createXViewGroupBox(self):
        self.XViewGroupBox = QGroupBox("Horizontal plane")
        # IMAGE
        self.imLabelX = QLabel()
        # SLIDER
        slider = QSlider(Qt.Horizontal, self.XViewGroupBox)
        slider.setMinimum(0)
        slider.setMaximum(self.imageShape[0]-1)
        slider.valueChanged.connect(self.setX)
        # INDEX
        self.idxLabelX = QLabel()

        # initialization
        self.setX(0)
        # LAYOUT
        layout = QVBoxLayout()
        layout.addWidget(self.idxLabelX)
        layout.addWidget(self.imLabelX)
        layout.addWidget(slider)
        layout.addStretch(1)
        self.XViewGroupBox.setLayout(layout)

    def createYViewGroupBox(self):
        self.YViewGroupBox = QGroupBox("Coronal plane")
        # IMAGE
        self.imLabelY = QLabel()
        # SLIDER
        slider = QSlider(Qt.Horizontal, self.YViewGroupBox)
        slider.setMinimum(0)
        slider.setMaximum(self.imageShape[1]-1)
        slider.valueChanged.connect(self.setY)
        # INDEX
        self.idxLabelY = QLabel()

        # initialization
        self.setY(0)
        # LAYOUT
        layout = QVBoxLayout()
        layout.addWidget(self.idxLabelY)
        layout.addWidget(self.imLabelY)
        layout.addWidget(slider)
        layout.addStretch(1)
        self.YViewGroupBox.setLayout(layout)

    def createZViewGroupBox(self):
        self.ZViewGroupBox = QGroupBox("Sagittal plane")
        # IMAGE
        self.imLabelZ = QLabel()
        # SLIDER
        slider = QSlider(Qt.Horizontal, self.ZViewGroupBox)
        slider.setMinimum(0)
        slider.setMaximum(self.imageShape[2]-1)
        slider.valueChanged.connect(self.setZ)
        # INDEX
        self.idxLabelZ = QLabel()

        # initialization
        self.setZ(0)
        # LAYOUT
        layout = QVBoxLayout()
        layout.addWidget(self.idxLabelZ)
        layout.addWidget(self.imLabelZ)
        layout.addWidget(slider)
        layout.addStretch(1)
        self.ZViewGroupBox.setLayout(layout)

    def createInfoGroupBox(self):
        self.infoGroupBox = QGroupBox("Information")

        self.HistoLabel = QLabel()
        image = self.imageData.getHistogram()
        self.HistoLabel.setPixmap(
            ndarrayToQPixmap(image, QImage.Format_RGB888))
        layout = QVBoxLayout()
        layout.addWidget(self.HistoLabel)
        self.infoGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    gallery = SimpleITKSnap("CTA.nii.gz")
    gallery.show()
    sys.exit(app.exec_())