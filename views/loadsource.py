import sys

from PySide2.QtWidgets import QFileDialog, QApplication, QMainWindow
from PySide2.QtGui import QPixmap
from PySide2.QtUiTools import QUiLoader

import window

class ImageFile:
    def __init__(self):
        self.imageObj = None

    # Set image object
    def setImage(self, imageObj):
        self.imageObj = imageObj

    # Load image
    def loadImage(self):
        print("image")
        frame = QFileDialog.getOpenFileName()
        #pixmapVar = QPixmap()
        #pixmapVar.load(frame[0])
        self.setImage(frame[0])
        if self.imageObj is not None:
            print("it's exists!!")

        return frame

        # app = QApplication.instance()
        # for widget in app.topLevelWidgets():
        #     if isinstance(widget, QMainWindow):
        #         widget.update()

        #window.
        #mainwidget.MyWidget().update()


    # Load Video
    def loadVideo(self):
        print("video")
