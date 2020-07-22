from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QDialog,
                             QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget)
from PyQt5.QtGui import QImage, QPixmap

from ViewModel import FileView3D, View3D
from utils.ImageIO import createQPixmapFromArray
from Extension import histogram, FFT
from PyQt5 import QtCore


class SimpleITKSnap(QDialog):
    def __init__(self, view: View3D):
        super(SimpleITKSnap, self).__init__()
        # load image
        self.imageData = view
        self.imageShape = self.imageData.data.shape

        self.x, self.y, self.z = 0, 0, 0
        self.extensionFunc = FFT
        self.createExtensionGroupBox()
        self.createXViewGroupBox()
        self.createYViewGroupBox()
        self.createZViewGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.XViewGroupBox, 1, 0)
        mainLayout.addWidget(self.YViewGroupBox, 1, 1)
        mainLayout.addWidget(self.ZViewGroupBox, 2, 0)
        mainLayout.addWidget(self.extensionGroupBox, 2, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("Simple-ITKSnap")

    def refreshExtension(self):
        image, text = self.imageData.getExtensionInfo(self.extensionFunc, self.x, self.y, self.z)
        self.extensionImageLabel.setPixmap(createQPixmapFromArray(image, fmt=QImage.Format_RGB888))
        self.extensionTextLabel.setText(text)

    def setX(self, x):
        self.x = x
        # IMAGE
        image = self.imageData.getXSlice(self.x)
        self.imLabelX.setPixmap(createQPixmapFromArray(image))
        # INDEX
        self.idxLabelX.setText("{}/{}".format(self.x + 1, self.imageShape[0]))
        # self.refreshExtension()

    def setY(self, y):
        self.y = y
        # IMAGE
        image = self.imageData.getYSlice(self.y)
        self.imLabelY.setPixmap(createQPixmapFromArray(image))
        # INDEX
        self.idxLabelY.setText("{}/{}".format(self.y + 1, self.imageShape[1]))
        # self.refreshExtension()

    def setZ(self, z):
        self.z = z
        # IMAGE
        image = self.imageData.getZSlice(self.z)
        self.imLabelZ.setPixmap(createQPixmapFromArray(image))
        # INDEX
        self.idxLabelZ.setText("{}/{}".format(self.z + 1, self.imageShape[2]))
        # self.refreshExtension()

    def createXViewGroupBox(self):
        self.XViewGroupBox = QGroupBox("Horizontal plane")
        # IMAGE
        self.imLabelX = QLabel()
        # SLIDER
        slider = QSlider(Qt.Horizontal, self.XViewGroupBox)
        slider.setMinimum(0)
        slider.setMaximum(self.imageShape[0] - 1)
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
        slider.setMaximum(self.imageShape[1] - 1)
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
        slider.setMaximum(self.imageShape[2] - 1)
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

    def createExtensionGroupBox(self):
        self.extensionGroupBox = QGroupBox("Extension")

        self.extensionImageLabel = QLabel()
        self.extensionTextLabel = QLabel()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)  # Throw event timeout with an interval of 500 milliseconds
        self.timer.timeout.connect(self.refreshExtension)
        self.timer.start()

        layout = QVBoxLayout()
        layout.addWidget(self.extensionImageLabel)
        layout.addWidget(self.extensionTextLabel)
        self.extensionGroupBox.setLayout(layout)
