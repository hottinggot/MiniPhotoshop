import cv2
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog, QWidget, QDesktopWidget, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QGroupBox, QCheckBox, QTableWidget, QLayout, QGridLayout, QSlider, QPushButton, QRadioButton, QButtonGroup
from PySide2.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPalette, QPixmap, QImage
from PySide2.QtCore import QPoint, QRect, Qt

from funcs import point_processing as pp
from funcs import histogram
from funcs import area_processing as ap

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
        saveAction.triggered.connect(self.save_image)

        # menu bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)

        filemenu = menubar.addMenu('&File')

        filemenu.addAction(loadImageAction)
        filemenu.addAction(loadVideoAction)
        filemenu.addAction(saveAction)




    def addGui(self):

        # Left: image box
        leftContainer = QWidget()
        leftContainer.setFixedSize(self.width() / 2 - 100, self.height() - 100)


        # 현재 이미지
        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize((self.width()/2) - 110, self.height()/2 - 110)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setText("Load Image")

        # 효과 적용 이미지
        self.processedImageLabel = QLabel()
        self.processedImageLabel.setFixedSize((self.width()/2) - 110, self.height()/2 - 110)
        self.processedImageLabel.setAlignment(Qt.AlignCenter)
        self.processedImageLabel.setText("Processed Image Area")

        leftImageLayout = QVBoxLayout()
        leftImageLayout.addWidget(self.imageLabel)
        leftImageLayout.addWidget(self.processedImageLabel)
        leftContainer.setLayout(leftImageLayout)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(leftContainer)


        # right: image processing option

        self.allgroup = QButtonGroup()
        # container
        container = QWidget()
        # container.setStyleSheet("background-color: white; ")
        container.setFixedSize(self.width()/2 - 100 , self.height() - 100)
        container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Photoshop title label
        titleLabel = QLabel("Photoshop Tools")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabelFont = titleLabel.font()
        titleLabelFont.setPointSize(25)
        titleLabel.setFont(titleLabelFont)

        # Effect title label
        sTitleLabel1 = QLabel("Effect")
        font1 = titleLabel.font()
        font1.setPointSize(18)
        sTitleLabel1.setFont(font1)


        # Negative radio button
        negative_groupbox = QGroupBox("반전")
        negative_radiobtn = QRadioButton("흑백 반전", self)

        font2 = negative_radiobtn.font()
        font2.setPointSize(13)
        negative_radiobtn.setFont(font2)
        negative_radiobtn.clicked.connect(self.negative_button_clicked)
        self.allgroup.addButton(negative_radiobtn)

        negative_layout = QHBoxLayout()
        negative_layout.addWidget(negative_radiobtn)
        negative_groupbox.setLayout(negative_layout)


        # Power law radio button
        powerlaw_groupbox= QGroupBox("Power law 변환", self)
        hbox = QHBoxLayout()
        powerlaw_radiobtn_1 = QRadioButton("0.01", self)
        powerlaw_radiobtn_2 = QRadioButton("0.1", self)
        powerlaw_radiobtn_3 = QRadioButton("0.5", self)
        powerlaw_radiobtn_4 = QRadioButton("5", self)
        powerlaw_radiobtn_5 = QRadioButton("10", self)
        powerlaw_radiobtn_6 = QRadioButton("25", self)
        self.allgroup.addButton(powerlaw_radiobtn_1)
        self.allgroup.addButton(powerlaw_radiobtn_2)
        self.allgroup.addButton(powerlaw_radiobtn_3)
        self.allgroup.addButton(powerlaw_radiobtn_4)
        self.allgroup.addButton(powerlaw_radiobtn_5)
        self.allgroup.addButton(powerlaw_radiobtn_6)
        powerlaw_radiobtn_1.clicked.connect(self.power_law_button_1_clicked)
        powerlaw_radiobtn_2.clicked.connect(self.power_law_button_2_clicked)
        powerlaw_radiobtn_3.clicked.connect(self.power_law_button_3_clicked)
        powerlaw_radiobtn_4.clicked.connect(self.power_law_button_4_clicked)
        powerlaw_radiobtn_5.clicked.connect(self.power_law_button_5_clicked)
        powerlaw_radiobtn_6.clicked.connect(self.power_law_button_6_clicked)


        hbox.addWidget(powerlaw_radiobtn_1)
        hbox.addWidget(powerlaw_radiobtn_2)
        hbox.addWidget(powerlaw_radiobtn_3)
        hbox.addWidget(powerlaw_radiobtn_4)
        hbox.addWidget(powerlaw_radiobtn_5)
        hbox.addWidget(powerlaw_radiobtn_6)
        powerlaw_groupbox.setLayout(hbox)


        # histogram equalization radio btn
        histeq_groupbox = QGroupBox("대비 개선")
        histeq_radiobtn = QRadioButton("히스토그램 평활화", self)
        histeq_radiobtn.setFont(font2)
        self.allgroup.addButton(histeq_radiobtn)
        histeq_layout = QHBoxLayout()
        histeq_layout.addWidget(histeq_radiobtn)
        histeq_groupbox.setLayout(histeq_layout)

        histeq_radiobtn.clicked.connect(self.histeq_button_clicked)


        # Filter title label
        sTitleLabel2 = QLabel("Filter")
        sTitleLabel2.setFont(font1)

        # mean filter
        mean_filter_groupbox = QGroupBox("Mean filter")
        mean_layout = QHBoxLayout()
        mean_radiobtn_1 = QRadioButton("3X3", self)
        mean_radiobtn_2 = QRadioButton("5X5", self)
        mean_radiobtn_3 = QRadioButton("7X7", self)
        self.allgroup.addButton(mean_radiobtn_1)
        self.allgroup.addButton(mean_radiobtn_2)
        self.allgroup.addButton(mean_radiobtn_3)
        mean_layout.addWidget(mean_radiobtn_1)
        mean_layout.addWidget(mean_radiobtn_2)
        mean_layout.addWidget(mean_radiobtn_3)

        mean_radiobtn_1.clicked.connect(self.mean_button_clicked_1)
        mean_radiobtn_2.clicked.connect(self.mean_button_clicked_2)
        mean_radiobtn_3.clicked.connect(self.mean_button_clicked_3)

        mean_filter_groupbox.setLayout(mean_layout)


        # gaussian filter
        gaussian_filter_groupbox = QGroupBox("Gaussian filter")
        gaussian_layout = QHBoxLayout()
        gaussian_radiobtn_1 = QRadioButton("3X3", self)
        gaussian_radiobtn_2 = QRadioButton("5X5", self)
        gaussian_radiobtn_3 = QRadioButton("7X7", self)
        self.allgroup.addButton(gaussian_radiobtn_1)
        self.allgroup.addButton(gaussian_radiobtn_2)
        self.allgroup.addButton(gaussian_radiobtn_3)
        gaussian_layout.addWidget(gaussian_radiobtn_1)
        gaussian_layout.addWidget(gaussian_radiobtn_2)
        gaussian_layout.addWidget(gaussian_radiobtn_3)

        gaussian_filter_groupbox.setLayout(gaussian_layout)

        gaussian_radiobtn_1.clicked.connect(self.gaussian_button_clicked_1)
        gaussian_radiobtn_2.clicked.connect(self.gaussian_button_clicked_2)
        gaussian_radiobtn_3.clicked.connect(self.gaussian_button_clicked_3)


        # median filter
        median_filter_groupbox = QGroupBox("Median filter")
        median_layout = QHBoxLayout()
        median_radiobtn_1 = QRadioButton("3X3", self)
        median_radiobtn_2 = QRadioButton("5X5", self)
        self.allgroup.addButton(median_radiobtn_1)
        self.allgroup.addButton(median_radiobtn_2)
        median_layout.addWidget(median_radiobtn_1)
        median_layout.addWidget(median_radiobtn_2)
        median_filter_groupbox.setLayout(median_layout)

        median_radiobtn_1.clicked.connect(self.median_button_clicked_1)
        median_radiobtn_2.clicked.connect(self.median_button_clicked_2)

        highboost_filter_groupbox = QGroupBox("Highboost filter")
        highboost_layout = QHBoxLayout()
        highboost_radio_button_1 = QRadioButton("type1", self)
        highboost_radio_button_2 = QRadioButton("type2", self)
        self.allgroup.addButton(highboost_radio_button_1)
        self.allgroup.addButton(highboost_radio_button_2)
        highboost_layout.addWidget(highboost_radio_button_1)
        highboost_layout.addWidget(highboost_radio_button_2)
        highboost_filter_groupbox.setLayout(highboost_layout)

        highboost_radio_button_1.clicked.connect(self.highboost_button_clicked_1)
        highboost_radio_button_2.clicked.connect(self.highboost_button_clicked_2)

        edge_groupbox = QGroupBox("선 추출")
        edge_layout = QHBoxLayout()

        # Prewitt radio button
        prewitt_radiobtn = QRadioButton("Prewitt")
        prewitt_radiobtn.setFont(font2)
        self.allgroup.addButton(prewitt_radiobtn)

        # Sobel radio button
        sobel_radiobtn = QRadioButton("Sobel")
        sobel_radiobtn.setFont(font2)
        self.allgroup.addButton(sobel_radiobtn)

        # LoG radio button
        log_radiobtn = QRadioButton("LoG")
        log_radiobtn.setFont(font2)
        self.allgroup.addButton(log_radiobtn)

        edge_layout.addWidget(prewitt_radiobtn)
        edge_layout.addWidget(sobel_radiobtn)
        edge_layout.addWidget(log_radiobtn)
        edge_groupbox.setLayout(edge_layout)

        prewitt_radiobtn.clicked.connect(self.prewitt_button_clicked)
        sobel_radiobtn.clicked.connect(self.sobel_button_clicked)
        log_radiobtn.clicked.connect(self.LoG_button_clicked)

        # 적용하기 버튼
        self.changeButton = QCheckBox("적용하기", self)
        self.changeButton.clicked.connect(self.change_button_clicked)

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
        rightGridLayout.addWidget(negative_groupbox, 3, 0, 1, 1)
        rightGridLayout.addWidget(powerlaw_groupbox, 4, 0, 1, -1)
        rightGridLayout.addWidget(histeq_groupbox, 6, 0, 1, 1)
        rightGridLayout.addWidget(sTitleLabel2, 7, 0, 1, 1)
        rightGridLayout.addWidget(mean_filter_groupbox, 8, 0, 1, -1)
        rightGridLayout.addWidget(gaussian_filter_groupbox, 9, 0, 1, -1)
        rightGridLayout.addWidget(median_filter_groupbox, 10, 0, 1, -1)
        rightGridLayout.addWidget(highboost_filter_groupbox, 11, 0, 1, -1)
        rightGridLayout.addWidget(edge_groupbox, 12, 0, 1, -1)
        rightGridLayout.addWidget(self.changeButton, 13, 0, 5, 1)

        self.imageLabel.setStyleSheet("background-color: lightgray;")
        self.processedImageLabel.setStyleSheet("background-color: lightgray;")

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)

        ll = QWidget()
        ll.setLayout(layout)
        self.setCentralWidget(ll)


    def open_image(self):
        frame = QFileDialog.getOpenFileName()

        # set imageVar
        self.imageVar = QImage()
        self.imageVar.load(frame[0])

        # set originImgArr
        height = self.imageVar.height()
        width = self.imageVar.width()
        ptr = self.imageVar.constBits()
        ptr = self.imageVar.constBits()

        if self.imageVar.format() == QImage.Format_RGB32 or self.ㅜimageVar.format() == QImage.Format_ARGB32:
            self.originImgArr = np.array(ptr).reshape(height, width, 4)
        else:
            self.originImgArr = np.array(ptr).reshape(height, width)

        # set image label with pixmap
        pixmapVar = QPixmap.fromImage(self.imageVar)

        newWidth = (self.width() / 2) - 110
        newHeight = (self.height() / 2) - 110
        widthRatio = pixmapVar.width()  / newWidth
        heightRatio = pixmapVar.height() / newHeight
        if widthRatio >= heightRatio:
            self.imageLabel.setFixedSize(newWidth, pixmapVar.height()/widthRatio)
            pixmapVar.scaledToWidth(self.imageLabel.width(), Qt.SmoothTransformation)
        else:
            self.imageLabel.setFixedSize(pixmapVar.width()/heightRatio, newHeight)
            pixmapVar.scaledToHeight(self.imageLabel.height(), Qt.SmoothTransformation)

        self.imageLabel.setPixmap(pixmapVar)
        self.imageLabel.setScaledContents(True)


    def set_processed_image(self, image):
        height = image.shape[0]
        width = image.shape[1]
        self.processedImageArr = image
        self.processedImageVar = QImage(image.data, width, height, width, QImage.Format_Grayscale8)

        pixmapVar = QPixmap.fromImage(self.processedImageVar)

        newWidth = (self.width() / 2) - 110
        newHeight = (self.height() / 2) - 110
        widthRatio = pixmapVar.width() / newWidth
        heightRatio = pixmapVar.height() / newHeight
        if widthRatio >= heightRatio:
            self.processedImageLabel.setFixedSize(newWidth, pixmapVar.height() / widthRatio)
            pixmapVar.scaledToWidth(self.processedImageLabel.width(), Qt.SmoothTransformation)
        else:
            self.processedImageLabel.setFixedSize(pixmapVar.width() / heightRatio, newHeight)
            pixmapVar.scaledToHeight(self.processedImageLabel.height(), Qt.SmoothTransformation)

        self.processedImageLabel.setPixmap(pixmapVar)
        self.processedImageLabel.setScaledContents(True)


    def newset_original_image(self, image):
        #self.originImgArr = image
        height = image.shape[0]
        width = image.shape[1]
        self.imageVar = QImage(image.data, width, height, width, QImage.Format_Grayscale8)

        # set image label with pixmap
        pixmapVar = QPixmap.fromImage(self.imageVar)

        newWidth = (self.width() / 2) - 110
        newHeight = (self.height() / 2) - 110
        widthRatio = pixmapVar.width() / newWidth
        heightRatio = pixmapVar.height() / newHeight
        if widthRatio >= heightRatio:
            self.imageLabel.setFixedSize(newWidth, pixmapVar.height() / widthRatio)
            pixmapVar.scaledToWidth(self.imageLabel.width(), Qt.SmoothTransformation)
        else:
            self.imageLabel.setFixedSize(pixmapVar.width() / heightRatio, newHeight)
            pixmapVar.scaledToHeight(self.imageLabel.height(), Qt.SmoothTransformation)

        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setPixmap(pixmapVar)
        self.imageLabel.setScaledContents(True)

        # set originImgArr
        height = self.imageVar.height()
        width = self.imageVar.width()
        ptr = self.imageVar.constBits()
        if self.imageVar.format() == QImage.Format_RGB32:
            self.originImgArr = np.array(ptr).reshape(height, width, 4)
        else:
            self.originImgArr = np.array(ptr).reshape(height, width)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def negative_button_clicked(self):
        self.set_processed_image(pp.negative_func(self.originImgArr))

    def power_law_button_1_clicked(self):
        self.set_processed_image(pp.power_law_func(self.originImgArr, gamma=0.01))

    def power_law_button_2_clicked(self):
        self.set_processed_image(pp.power_law_func(self.originImgArr, gamma=0.1))

    def power_law_button_3_clicked(self):
        self.set_processed_image(pp.power_law_func(self.originImgArr, gamma=0.5))

    def power_law_button_4_clicked(self):
        self.set_processed_image(pp.power_law_func(self.originImgArr, gamma=5))

    def power_law_button_5_clicked(self):
        self.set_processed_image(pp.power_law_func(self.originImgArr, gamma=10))

    def power_law_button_6_clicked(self):
        self.set_processed_image(pp.power_law_func(self.originImgArr, gamma=25))

    def histeq_button_clicked(self):
        self.set_processed_image(histogram.hist_equalization(self.originImgArr))

    def mean_button_clicked_1(self):
        self.set_processed_image(ap.mean_filter(self.originImgArr, mask=1))

    def mean_button_clicked_2(self):
        self.set_processed_image(ap.mean_filter(self.originImgArr, mask=2))

    def mean_button_clicked_3(self):
        self.set_processed_image(ap.mean_filter(self.originImgArr, mask=3))

    def gaussian_button_clicked_1(self):
        self.set_processed_image(ap.gaussian_filter(self.originImgArr, mask=1, sigma=1))

    def gaussian_button_clicked_2(self):
        self.set_processed_image(ap.gaussian_filter(self.originImgArr, mask=2, sigma=1))

    def gaussian_button_clicked_3(self):
        self.set_processed_image(ap.gaussian_filter(self.originImgArr, mask=3, sigma=1))

    def median_button_clicked_1(self):
        self.set_processed_image(ap.median_filter(self.originImgArr, mask=1))

    def median_button_clicked_2(self):
        self.set_processed_image(ap.median_filter(self.originImgArr, mask=2))

    def highboost_button_clicked_1(self):
        self.set_processed_image(ap.highboost_filter(self.originImgArr, a=1, filter_type=1))

    def highboost_button_clicked_2(self):
        self.set_processed_image(ap.highboost_filter(self.originImgArr, a=1, filter_type=2))

    def prewitt_button_clicked(self):
        self.set_processed_image(ap.prewitt_filter(self.originImgArr, threshold=100))

    def sobel_button_clicked(self):
        self.set_processed_image(ap.sobel_filter(self.originImgArr, threshold=100))

    def LoG_button_clicked(self):
        self.set_processed_image(ap.LoG_filter(self.originImgArr, mask=2, sigma=1))

    def change_button_clicked(self):
        self.newset_original_image(self.processedImageArr)
        self.changeButton.setCheckState(Qt.Unchecked)

        checked = self.allgroup.checkedButton()
        self.allgroup.setExclusive(False)
        checked.setChecked(False)
        self.allgroup.setExclusive(True)

    def save_image(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        self.imageVar.save(name)







