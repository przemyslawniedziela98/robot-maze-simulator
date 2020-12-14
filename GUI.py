# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGroupBox, QLineEdit, QPushButton, QTextBrowser, QSlider, QFileDialog, QCheckBox
from PyQt5.QtGui import  QFont, QIcon,QPixmap
from PyQt5.QtCore import QRect, Qt
import sys
import os
from MAZE import Maze
from mapping import mapping
from PLAY import game
from directions_mapping import communication
import time 

class App(QWidget):
    def __init__(self):
        # init main ui window
        super().__init__()
        self.title = 'Symulator pokonywania labiryntu'
        self.left = 100
        self.top = 100
        self.width = 920
        self.height = 680

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(App.resource_path("AGH.png")))
        
        self.file = "LABIRYNT.png"
        
        self.label = QLabel(self)
        self.label.setGeometry(QRect(140, 42, 760, 60))
        font = QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("Symulator pokonywania labiryntu")
        
        self.image = QLabel(self)
        self.image.setGeometry(QRect(20, 20, 100, 100))
        pixmap = QPixmap(App.resource_path('AGH.png'))
        pixmap = pixmap.scaledToHeight(100)
        self.image.setPixmap(pixmap)
        
        self.groupBox_generator = QGroupBox(self)
        self.groupBox_generator.setGeometry(QRect(42, 140, 410, 155))
        self.groupBox_generator.setTitle("Generator labiryntu:")
        
        self.textBrowser_wall_thick = QLineEdit(self.groupBox_generator)
        self.textBrowser_wall_thick.setGeometry(QRect(10,30, 160, 30))
        self.textBrowser_wall_thick.setPlaceholderText("grubosc scianki [mm]")
        
        self.textBrowser_wall_dimension = QLineEdit(self.groupBox_generator)
        self.textBrowser_wall_dimension.setGeometry(QRect(180,30, 220, 30))
        self.textBrowser_wall_dimension.setPlaceholderText("odleglosc miedzy sciankami [mm]")
        
        self.textBrowser_x_number = QLineEdit(self.groupBox_generator)
        self.textBrowser_x_number.setGeometry(QRect(10,70, 390, 30))
        self.textBrowser_x_number.setPlaceholderText("ilosc pol poziomo i pionowo")
        
        
        
        self.pushButton_load_directory = QPushButton(self.groupBox_generator)
        self.pushButton_load_directory.setGeometry(QRect(220, 110, 70, 30))
        self.pushButton_load_directory.setText("Wybierz")
        self.pushButton_load_directory.clicked.connect(self.set_directory)
        
        self.textBrowser_load_directory = QTextBrowser(self.groupBox_generator)
        self.textBrowser_load_directory.setGeometry(QRect(10, 110, 200, 30))
        self.textBrowser_load_directory.setPlaceholderText("lokalizacja pliku")
        
        self.pushButton_load_dwg = QPushButton(self.groupBox_generator)
        self.pushButton_load_dwg.setGeometry(QRect(220, 110, 70, 30))
        self.pushButton_load_dwg.setText("Wybierz")
        self.pushButton_load_dwg.clicked.connect(self.set_directory)
        
        self.pushButton_genr = QPushButton(self.groupBox_generator)
        self.pushButton_genr.setGeometry(QRect(300, 110, 100, 30))
        self.pushButton_genr.setText("generuj")
        self.pushButton_genr.clicked.connect(self.connect_to_maze)
        
        self.groupBox_generator_map= QGroupBox(self)
        self.groupBox_generator_map.setGeometry(QRect(42, 310, 410, 145))
        self.groupBox_generator_map.setTitle("Generator mapowania:")
        
        self.textBrowser_precision = QLineEdit(self.groupBox_generator_map)
        self.textBrowser_precision.setGeometry(QRect(10,30, 160, 30))
        self.textBrowser_precision.setPlaceholderText("dokladnosc [mm]")
        
        self.checkBox_map01 = QCheckBox(self.groupBox_generator_map)
        self.checkBox_map01.setGeometry(QRect(10, 70, 170, 20))
        self.checkBox_map01.setText("mapowanie obszaru 0/1")

        self.checkBox_pos_txt = QCheckBox(self.groupBox_generator_map)
        self.checkBox_pos_txt.setGeometry(QRect(190, 70, 180, 20))
        self.checkBox_pos_txt.setText("pozycje przeszkod [mm]")

        self.label = QLabel(self.groupBox_generator_map)
        self.label.setGeometry(QRect(180, 15, 760, 60))
        self.label.setText("mininalna dokladnosc - 1 mm")
        
        self.pushButton_load_directory_map = QPushButton(self.groupBox_generator_map)
        self.pushButton_load_directory_map.setGeometry(QRect(220, 100, 70, 30))
        self.pushButton_load_directory_map.setText("Wybierz")
        self.pushButton_load_directory_map.clicked.connect(self.set_directory_map)
        
        self.pushButton_load_directory_map = QTextBrowser(self.groupBox_generator_map)
        self.pushButton_load_directory_map.setGeometry(QRect(10, 100, 200, 30))
        self.pushButton_load_directory_map.setPlaceholderText("lokalizacja pliku")
        
        self.pushButton_genr = QPushButton(self.groupBox_generator_map)
        self.pushButton_genr.setGeometry(QRect(300, 100, 100, 30))
        self.pushButton_genr.setText("generuj")
        self.pushButton_genr.clicked.connect(self.connect_to_mapping)
        
        self.groupBox_manual = QGroupBox(self)
        self.groupBox_manual.setGeometry(QRect(42, 470, 410, 70))
        self.groupBox_manual.setTitle("Tryb Manualny:")
        
        self.label = QLabel(self.groupBox_manual)
        self.label.setGeometry(QRect(10, 15, 80, 60))
        self.label.setText("Predkosc:")
        
        self.slider_speed = QSlider(Qt.Horizontal, self.groupBox_manual)
        self.slider_speed.setGeometry(QRect(80, 31, 230, 30))
        self.slider_speed.setRange(2, 12)
        
        self.start = QPushButton(self.groupBox_manual)
        self.start.setGeometry(QRect(320, 31, 80, 30))
        self.start.setText("start")
        self.start.clicked.connect(self.connect_to_play)
        
        self.image = QLabel(self)
        self.image.setGeometry(QRect(480, 160, 380, 380))
        self.pixmap = QPixmap(App.resource_path(self.file))
        self.pixmap = self.pixmap.scaledToHeight(380)
        self.image.setPixmap(self.pixmap)
        
        self.groupBox_automat= QGroupBox(self)
        self.groupBox_automat.setGeometry(QRect(42, 550, 820, 70))
        self.groupBox_automat.setTitle("Tryb automatyczny z Arduino:")
        
        self.label = QLabel(self.groupBox_automat)
        self.label.setGeometry(QRect(10, 15, 80, 60))
        self.label.setText("Predkosc:")
        
        self.slider_speed_automat = QSlider(Qt.Horizontal, self.groupBox_automat)
        self.slider_speed_automat.setGeometry(QRect(80, 31, 230, 30))
        self.slider_speed_automat.setRange(2, 12)
        
        self.textBrowser_port = QLineEdit(self.groupBox_automat)
        self.textBrowser_port.setGeometry(QRect(320 ,30, 100, 30))
        self.textBrowser_port.setPlaceholderText("port szeregowy")
        
        self.textBrowser_port = QLineEdit(self.groupBox_automat)
        self.textBrowser_port.setGeometry(QRect(320 ,30, 120, 30))
        self.textBrowser_port.setPlaceholderText("port szeregowy")
        
        self.textBrowser_baud_rate = QLineEdit(self.groupBox_automat)
        self.textBrowser_baud_rate.setGeometry(QRect(450 ,30, 210, 30))
        self.textBrowser_baud_rate.setPlaceholderText("predkosc transmisji")
        
        self.start_automat = QPushButton(self.groupBox_automat)
        self.start_automat.setGeometry(QRect(680, 31, 120, 30))
        self.start_automat.setText("start")
        self.start_automat.clicked.connect(self.connect_to_automatic)
        
        self.show()
        
    def connect_to_play(self):
        xy_value = int(self.textBrowser_wall_dimension.text()) * int(self.textBrowser_x_number.text()) + 2*int(self.textBrowser_wall_thick.text())
        game.set_image(xy_value, xy_value, self.filename, self.slider_speed.value(),  
                       int(self.textBrowser_wall_dimension.text()))
    def connect_to_automatic(self):
        #communication.create_walls_info(self.filename, int(self.textBrowser_wall_dimension.text()), int(self.textBrowser_wall_thick.text()), self.textBrowser_port.text(),int(self.textBrowser_baud_rate.text()))
        time.sleep(3)
        xy_value = int(self.textBrowser_wall_dimension.text()) * int(self.textBrowser_x_number.text()) + 2*int(self.textBrowser_wall_thick.text())
        game.set_image(xy_value, xy_value, self.filename, self.slider_speed_automat.value(),  
                       int(self.textBrowser_wall_dimension.text()))
        
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)
    
    def connect_to_maze(self):
        App.create_filename(self)
        maze = Maze(int(self.textBrowser_x_number.text()), int(self.textBrowser_x_number.text()))
        maze.make_maze()
        maze.create_output_file(self.filename, int(self.textBrowser_wall_dimension.text()), int(self.textBrowser_wall_thick.text()))
        self.pixmap = QPixmap(self.filename)
        self.pixmap = self.pixmap.scaledToHeight(380)
        self.image.setPixmap(self.pixmap)
        
    def connect_to_mapping(self):
        mapping.get_pixcels(self.filename, int(self.textBrowser_precision.text()), self.checkBox_map01.isChecked(), 
                            self.checkBox_pos_txt.isChecked(), self.directory_map)
        
        
    def create_filename(self):
        name = "LABIRYNT.png" 
        if os.path.isfile(name):
            n=0
            while os.path.isfile(name):
                n+=1 
                name = "LABIRYNT_" + str(n)+'.png' 
        self.filename = self.directory + '//'+ name
        
    def set_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.directory:
            self.textBrowser_load_directory.setText(self.directory)
            
    def set_directory_map(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.directory_map = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.directory_map:
            self.pushButton_load_directory_map.setText(self.directory)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())