from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QWidget, QDesktopWidget, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QGroupBox, QCheckBox, QTableWidget, QLayout
from PySide2.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath, QPalette, QPixmap
from PySide2.QtCore import QPoint, QRect, Qt

from views import loadsource
from views import imageView

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        # Add all GUI Elements to Class

        self.addMenu()
        self.addGui()
        #self.wg = mainwidget.MyWidget()
        #self.setCentralWidget(self.wg)

        self.resize(1200, 750)
        self.center()
        self.setWindowTitle('Mini Photoshop')
        self.show()


    def addMenu(self):
        # File menu
        loadImageAction = QAction('Load Image...', self)
        #loadImageAction.setStatusTip('Open JPEG Image')
        loadImageAction.triggered.connect(self.updateImage)

        loadVideoAction = QAction('Load Video...', self)
        #loadVideoAction.setStatusTip('Open Video')

        saveAction = QAction('Save as...', self)
        #saveAction.setStatusTip('Save as specific name')

        # histogram
        drawOneDimHistAction = QAction('Draw histogram ver.1', self)
        #drawOneDimHistAction.setStatusTip('Draw one dimension histogram')

        drawTwoDimHistAction = QAction('Draw histogram ver.2', self)
        #drawTwoDimHistAction.setStatusTip('Draw one dimension histogram at color space')

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
        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(300, 300)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        #self.imageLabel.setText("hello")
        #self.imageLabel.resize(50, 50)
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.imageLabel)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.imageLabel)

        self.imagefile = loadsource.ImageFile()
        if self.imagefile.imageObj is None:
            print("none!!")
            self.imageLabel.setStyleSheet("background-color: red;")
        else:
            # self.imageLabel.setStyleSheet("background-color: none;")
            self.imageLabel.setPixmap(imagefile.imageObj)
            # self.imageLabel.setText("hihihi")
            self.imageLabel.resize(imagefile.imageObj.width(), imagefile.imageObj.height())

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)

        ll = QWidget()
        ll.setLayout(layout)
        self.setCentralWidget(ll)

    def updateImage(self):
        imageName = loadsource.ImageFile().loadImage()

        pixmapVar = QPixmap()
        size = self.size()
        #pixmapVar.scaled(size, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        pixmapVar.load(imageName[0])

        ratio = pixmapVar.height() / pixmapVar.width()
        self.imageLabel.setFixedSize(self.width()/2, self.width()*ratio/2)
        pixmapVar.scaledToHeight(self.imageLabel.height(), Qt.SmoothTransformation)
        self.imageLabel.setPixmap(pixmapVar)
        self.imageLabel.setScaledContents(True)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
