import os
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from GUI import Ui_MainWindow
from myVideoWidget import myVideoWidget
import sys
import time
import ui_utility


def load_project_structure(startpath, tree):
    for element in os.listdir(startpath):
        path_info = startpath + "/" + element
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        if os.path.isdir(path_info):
            load_project_structure(path_info, parent_itm)
            parent_itm.setIcon(0, QIcon('assets/folder.ico'))
        else:
            parent_itm.setIcon(0, QIcon('assets/file.ico'))


class MyMainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.videoFullScreen = False   # 判断当前widget是否全屏
        self.videoFullScreenWidget = myVideoWidget()   # 创建一个全屏的widget
        self.videoFullScreenWidget.setFullScreen(1)
        self.videoFullScreenWidget.hide()
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)  # widget to play video
        self.btn_open.clicked.connect(self.open_video_file)   # open video file
        self.btn_analyse.clicked.connect(self.analyse)
        self.btn_play.clicked.connect(self.play_video)       # play
        self.btn_stop.clicked.connect(self.pause_video)       # pause
        self.player.positionChanged.connect(self.change_slide)      # change Slide
        self.videoFullScreenWidget.doubleClickedItem.connect(self.video_double_clicked)  #双击响应
        self.wgt_video.doubleClickedItem.connect(self.video_double_clicked)   #双击响应
        self.file_path = ""
        self.label.setText("image preview")
        self.treeView.doubleClicked.connect(self.tree_clicked)
        self.model = QDirModel()
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(r'./'))  #设置该路径为当前根路径
        

    def open_video_file(self):
        file_path = QFileDialog.getOpenFileUrl()[0]
        self.player.setMedia(QMediaContent(file_path))  # 选取视频文件
        self.player.play()  # 播放视频
        self.file_path = file_path.toString()

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def change_slide(self, position):
        self.vidoeLength = self.player.duration()+0.1
        self.sld_video.setValue(round(position/self.vidoeLength*100))
        self.lab_video.setText(str(round((position/self.vidoeLength)*100,2))+'%')

    def video_double_clicked(self, text):
        if self.player.duration() > 0:  # 开始播放后才允许进行全屏操作
            if self.videoFullScreen:
                self.player.pause()
                self.videoFullScreenWidget.hide()
                self.player.setVideoOutput(self.wgt_video)
                self.player.play()
                self.videoFullScreen = False
            else:
                self.player.pause()
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.player.play()
                self.videoFullScreen = True

    def analyse(self):
        if self.file_path == '':
            print('error, no selected file')
        else:
            video_path = self.file_path[7:]
            ui_utility.frame_cutting(video_path)
            video_name = ui_utility.get_video_name(self.file_path)
            '''
            frames are stored in '/(video_name)/'
            more code to be add to run the neural network
            '''
            self.model = QDirModel()
            self.treeView.setModel(self.model)
            self.treeView.setRootIndex(self.model.index(r'./'))
            
            
    def tree_clicked(self, Qmodelidx):
        clicked_file_path = self.model.filePath(Qmodelidx)
        pixmap = QPixmap(clicked_file_path)
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))
        self.label.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_gui = MyMainWindow()
    #load_project_structure('.', video_gui.treeWidget)
    video_gui.showMaximized()
    sys.exit(app.exec_())
    
