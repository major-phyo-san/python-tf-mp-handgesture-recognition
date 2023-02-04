import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QAction, qApp, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon
from Backend import HandGesturesDetector


class AppLayout(QMainWindow):
    appTitle = "Hand Gestures Detector"
    appMarginLeft = 100
    appMarginTop = 100
    appWidth = 640
    appHeight = 480
    
    gesturesDetector = HandGesturesDetector()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.appTitle)
        self.setGeometry(self.appMarginLeft, self.appMarginTop, self.appWidth, self.appHeight)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Z')
        exitAct.setStatusTip('Exit Appliction')
        exitAct.triggered.connect(qApp.quit)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(exitAct)

        self.addWidgets()
        
    def addWidgets(self):
        self.statusBar().showMessage('Ready')
        self.centralWidget = QWidget(self)
        vBoxLayout = QHBoxLayout()
        self.centralWidget.setLayout(vBoxLayout)
        self.setCentralWidget(self.centralWidget)

        self.startBtn = QPushButton("Star Detector")
        self.startBtn.clicked.connect(self.startDetector)
        vBoxLayout.addWidget(self.startBtn)

        self.closeBtn = QPushButton("Stop Detector")
        self.closeBtn.clicked.connect(self.stopDetector)
        vBoxLayout.addWidget(self.closeBtn)
        
    def startDetector(self):
        print('start')
        self.gesturesDetector.startDetector()
        
        
    def stopDetector(self):
        print('stop')
        self.gesturesDetector.stopDetector(True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppLayout()
    ex.show()
    sys.exit(app.exec_())

