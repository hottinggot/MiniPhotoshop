import cv2
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog, QWidget, QDesktopWidget, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QGroupBox, QCheckBox, QTableWidget, QLayout, QGridLayout, QSlider
from PySide2.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPalette, QPixmap, QImage
from PySide2.QtCore import QPoint, QRect, Qt

from views import loadsource
from views import imageView
from funcs import point_processing as pp

import qimage2ndarray
import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        # Add all GUI Elements to Class

        self.setFixedSize(1200, 750)

        self.addMenu()
        self.addGui()

        self.center()
        self.setWindowTitle('Mini Photoshop')
        self.show()


    def addMenu(self):
        # File menu
        loadImageAction = QAction('Load Image...', self)
        loadImageAction.triggered.connect(self.open_image)

        loadVideoAction = QAction('Load Video...', self)

        saveAction = QAction('Save as...', self)

        # histogram
        drawOneDimHistAction = QAction('Draw histogram ver.1', self)

        drawTwoDimHistAction = QAction('Draw histogram ver.2', self)

        # menu bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)

        filemenu = menubar.addMenu('&File')

        filemenu.addAction(loadImageAction)
        filemenu.addAction(loadVideoAction)
        filemenu.addAction(saveAction)

        histmenu = menubar.addMenu('&histogram')

        histmenu.addAction(drawOneDimHistAction)
        histmenu.addAction(drawTwoDimHistAction)

    def addGui(self):

        # Left - image box

        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize((self.width()/2) - 40, self.height()/2 - 40)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setText("Load Image")

        self.processedImageLabel = QLabel()
        self.processedImageLabel.setFixedSize((self.width()/2) - 40, self.height()/2 - 40)
        self.processedImageLabel.setAlignment(Qt.AlignCenter)
        self.processedImageLabel.setText("Processed Image Area")

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.imageLabel)
        leftLayout.addWidget(self.processedImageLabel)

        # right - image processing option

        # container
        container = QWidget()
        container.setStyleSheet("background-color: lightgray; ")
        container.setFixedSize(self.width()/2 - 100 , self.height() - 100)
        container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        #container.setAlignment(Qt.AlignRight)
        #container.setScaledContents(True)


        # Title label
        titleLabel = QLabel("Edit Tools")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabelFont = titleLabel.font()
        titleLabelFont.setPointSize(25)
        titleLabel.setFont(titleLabelFont)

        # s_title label
        sTitleLabel1 = QLabel("Effect")
        font1 = titleLabel.font()
        font1.setPointSize(18)
        sTitleLabel1.setFont(font1)

        # check box 1_1
        title1_checkbox1 = QCheckBox("Negative")
        font2 = title1_checkbox1.font()
        font2.setPointSize(13)
        title1_checkbox1.setFont(font2)
        # title1_checkbox1.stateChanged.connect(self.negativeFunc)
        title1_checkbox1.stateChanged.connect(self.negative_button_clicked)

        # check box 1_2
        title1_checkbox2 = QCheckBox("Power Law")
        title1_checkbox2.setFont(font2)

        # Gamma Slider
        self.slider = QSlider(Qt.Horizontal)

        self.slider.setMaximum(2500)
        self.slider.setMinimum(4)
        self.slider.setTickInterval(100)
        self.slider.setSingleStep(100)
        self.slider.setTickPosition(QSlider.TicksBelow)

        #self.slider.valueChanged.connect(self.testf)

        # check box 1_3
        title1_checkbox3 = QCheckBox("Histogram Equalization")
        title1_checkbox3.setFont(font2)

        # s_title label 2
        sTitleLabel2 = QLabel("Smoothing Filter")
        sTitleLabel2.setFont(font1)


        # check box 2_1
        title2_checkbox1 = QCheckBox("Mean")
        title2_checkbox1.setFont(font2)

        # check box 2_2
        title2_checkbox2 = QCheckBox("Gaussian")
        title2_checkbox2.setFont(font2)

        # check box 2_3
        title2_checkbox3 = QCheckBox("Median")
        title2_checkbox3.setFont(font2)

        # s_title label 3
        sTitleLabel3 = QLabel("Edge Detector")
        sTitleLabel3.setFont(font1)

        # check box 3_1
        title3_checkbox1 = QCheckBox("Prewitt")
        title3_checkbox1.setFont(font2)

        # check box 3_2
        title3_checkbox2 = QCheckBox("Sobel")
        title3_checkbox2.setFont(font2)

        # check box 3_3
        title3_checkbox3 = QCheckBox("LoG")
        title3_checkbox3.setFont(font2)

        # Empty box
        empty_box = QLabel()

        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(0)
        rightLayout.addWidget(container)

        rightGridLayout = QGridLayout()
        container.setLayout(rightGridLayout)

        row = 0
        col = 0
        rightGridLayout.addWidget(titleLabel, 0, 0, 2, -1)
        rightGridLayout.addWidget(sTitleLabel1, 2, 0, 1, 1)
        rightGridLayout.addWidget(title1_checkbox1, 3, 0, 1, -1)
        rightGridLayout.addWidget(title1_checkbox2, 4, 0, 1, -1)
        rightGridLayout.addWidget(self.slider, 5, 0, 1, 1)
        rightGridLayout.addWidget(title1_checkbox3, 6, 0, 1, 1)
        rightGridLayout.addWidget(sTitleLabel2, 7, 0, 1, 1)
        rightGridLayout.addWidget(title2_checkbox1, 8, 0, 1, 1)
        rightGridLayout.addWidget(title2_checkbox2, 8, 1, 1, 1)
        rightGridLayout.addWidget(title2_checkbox3, 8, 2, 1, 1)
        rightGridLayout.addWidget(sTitleLabel3, 9, 0, 1, 1)
        rightGridLayout.addWidget(title3_checkbox1, 10, 0, 1, 1)
        rightGridLayout.addWidget(title3_checkbox2, 10, 1, 1, 1)
        rightGridLayout.addWidget(title3_checkbox3, 10, 2, 1, 1)
        rightGridLayout.addWidget(empty_box, 11, 0, 5, -1)



        self.imagefile = loadsource.ImageFile()
        if self.imagefile.imageObj is None:
            self.imageLabel.setStyleSheet("background-color: lightgray;")
        else:
            self.imageLabel.setPixmap(imagefile.imageObj)
            self.imageLabel.resize(imagefile.imageObj.width(), imagefile.imageObj.height())

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)

        ll = QWidget()
        ll.setLayout(layout)
        self.setCentralWidget(ll)


    def set_image(self, image):
        height = image.shape[0]
        width = image.shape[1]
        self.imageVar = QImage(image.data, width, height, width, QImage.Format_Grayscale8)

        pixmapVar = QPixmap.fromImage(self.imageVar)
        self.imageLabel.setPixmap(pixmapVar)

    def open_image(self):
        frame = QFileDialog.getOpenFileName()

        # set imageVar
        self.imageVar = QImage()
        size = self.size()
        self.imageVar.load(frame[0])

        # set image label
        pixmapVar = QPixmap.fromImage(self.imageVar)

        ratio = pixmapVar.height() / pixmapVar.width()
        newWidth = (self.width()/2) - 40
        self.imageLabel.setFixedSize(newWidth, newWidth*ratio)
        pixmapVar.scaledToHeight(self.imageLabel.height(), Qt.SmoothTransformation)
        self.imageLabel.setPixmap(pixmapVar)
        self.imageLabel.setScaledContents(True)

        # set imageArr
        height = self.imageVar.height()
        width = self.imageVar.width()
        ptr = self.imageVar.constBits()
        self.imageArr = np.array(ptr).reshape(height, width, 4)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def negative_button_clicked(self):
        self.set_image(pp.negativeFunc(self.imageArr))

    def power_law_button_1_clicked(self):
        self.set_image(pp.powerLawFunc(self.imageArr, gamma=0.1))

