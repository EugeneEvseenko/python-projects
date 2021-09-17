import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog, 
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout,QMessageBox
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap  # оптимизированная для показа на экране картинка
from PIL import ImageEnhance
from PIL import Image
from PIL.ImageQt import ImageQt  # для перевода графики из Pillow в Qt
from PIL import ImageFilter
from PIL.ImageFilter import *
from PIL.ImageQt import ImageQt

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Выберите папку с файлами и откройте картинку")
btn_dir = QPushButton("Папка")
btn_update = QPushButton("Обновить", enabled = False)
lw_files = QListWidget()
lb_image_size = QLabel()
lb_image_format = QLabel()
lb_image_type = QLabel()

btn_left = QPushButton("Лево", enabled = False)
btn_right = QPushButton("Право", enabled = False)
btn_180 = QPushButton("180", enabled = False)
btn_flip = QPushButton("Зеркало", enabled = False)
btn_sharp = QPushButton("Резкость", enabled = False)
btn_contrast = QPushButton("Контраст", enabled = False)
btn_bw = QPushButton("Ч/Б", enabled = False)
btn_blur = QPushButton("Размытие", enabled = False)
btn_crop = QPushButton("Обрезка", enabled = False)

row = QHBoxLayout()          
col1 = QVBoxLayout()         
col2 = QVBoxLayout()
row_dir = QHBoxLayout() # горизонтальный слой для двух кнопок
row_dir.addWidget(btn_dir, 10) # папка
row_dir.addWidget(btn_update) # обновить
''' Кнопка сохранения, выключена сразу при создании'''
btn_save = QPushButton('Сохранить', enabled = False)
''' '''
row_info = QVBoxLayout()
row_info.addWidget(lb_image_size)
row_info.addWidget(lb_image_format)
row_info.addWidget(lb_image_type)
col1.addLayout(row_dir)      
col1.addWidget(lw_files) 
''' '''
col1.addWidget(btn_save) 
''' '''
col1.addLayout(row_info);
col2.addWidget(lb_image, 95)
tools_main = QHBoxLayout()
tools_secondary = QVBoxLayout()
row_tools1 = QHBoxLayout()  
row_tools2 = QHBoxLayout()   
row_tools1.addWidget(btn_left)
row_tools1.addWidget(btn_right)
row_tools1.addWidget(btn_180)
row_tools1.addWidget(btn_flip)
row_tools2.addWidget(btn_sharp)
row_tools2.addWidget(btn_contrast)
row_tools2.addWidget(btn_blur)
row_tools2.addWidget(btn_bw)
tools_secondary.addLayout(row_tools1)
tools_secondary.addLayout(row_tools2)
tools_main.addLayout(tools_secondary, 95)
tools_main.addWidget(btn_crop)
col2.addLayout(tools_main)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
win.show()

workdir = ''
def filter(files):
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    result = []
    for filename in files:
        for ext in extensions:
            if filename.lower().endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    if len(workdir) > 0: 
        return True # всё норм, папка выбрана, отправляем тру
    else:
        return False # не норм, ничего 

def showFilenamesList():
    if chooseWorkdir():
        filenames = filter(os.listdir(workdir))
        lw_files.clear()
        btn_update.setEnabled(True)
        ''' 
            Если пользователь выберет папку, то мы её запомним записав в файл
        '''
        with open("temp.txt", "w", encoding='utf-8') as file:
            file.write(workdir)
        for filename in filenames: # можно и так - lw_files.addItems(filenames)
            lw_files.addItem(filename) # это тоже надо убрать если хотите использовать пример из комментария выше

def set_enabled(enabled = True):
    btn_save.setEnabled(enabled)
    btn_left.setEnabled(enabled)
    btn_right.setEnabled(enabled)
    btn_180.setEnabled(enabled)
    btn_flip.setEnabled(enabled)
    btn_sharp.setEnabled(enabled)
    btn_contrast.setEnabled(enabled)
    btn_bw.setEnabled(enabled)
    btn_blur.setEnabled(enabled)
    btn_crop.setEnabled(enabled)

def update():
    global workdir
    set_enabled(False)
    if(os.path.exists("temp.txt")):
        with open("temp.txt", "r", encoding='utf-8') as file:
            workdir = file.read()
        if os.path.exists(workdir):
            btn_update.setEnabled(True)
            filenames = filter(os.listdir(workdir))
            lw_files.clear()
            for filename in filenames:
                lw_files.addItem(filename)
        else:
            os.remove('temp.txt')
            QMessageBox(QMessageBox.Information,
            "Упс!",
            "Сохраненный путь до прошлой папки больше не существует.").exec()
    else:
        btn_update.setEnabled(False)

def save_image():
    save_path = QFileDialog.getSaveFileName(
        caption = "Сохранение изображения",
        directory = os.path.join(workdir, workimage.filename), 
        filter = "Файлы изображений (*.jpg;*.jpeg;*.png;*.gif;*.bmp);;All Files (*)")
    if len(save_path[0]) > 0:
        workimage.saveImage(save_path[0])

update() 
btn_dir.clicked.connect(showFilenamesList)
btn_update.clicked.connect(update)
btn_save.clicked.connect(save_image)
class ImageProcessor:
    def __init__(self):
        self.image = None
        self.filename = None

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self, path):
        self.image.save(path)
        return path 

    def do_bw(self):
        self.image = self.image.convert("L")
        self.showImage()

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showImage()

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showImage()

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage()

    def do_sharpen(self):
        self.image = self.image.convert('RGB').filter(SHARPEN)
        self.showImage()

    def do_180(self):
        self.image = self.image.transpose(Image.ROTATE_180)
        self.showImage()

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.showImage()
    
    def do_contrast(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.5)
        self.showImage()

    def do_square(self):
        if self.image.size[0] != self.image.size[1]: # стороны равны
            box = (0,0,0,0)
            if self.image.size[0] > self.image.size[1]: # высота меньше ширины
                box = (0,0,self.image.size[1], self.image.size[1]) #лево, верх, право, низ
            else: # ширина меньше высоты
                box = (0,0,self.image.size[0], self.image.size[0]) #лево, верх, право, низ
            self.image = self.image.crop(box)
            self.showImage()
        else:
            QMessageBox(QMessageBox.Critical,
            "Ну ты чего!",
            "Я не могу сделать картинку ещё более квадратной!").exec()

    def showImage(self):
        im = self.image
        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif  im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
        
        lb_image.hide()
        pixmapimage = QPixmap(QPixmap.fromImage(qim))
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
        lb_image_size.setText(f"Размер: {self.image.size[0]}x{self.image.size[1]}")
        lb_image_format.setText(f"Формат: {self.image.format}")
        lb_image_type.setText(f"Тип: {self.image.mode}")

def showChosenImage():
    set_enabled()
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage()

workimage = ImageProcessor()  # текущая рабочая картинка для работы
lw_files.itemClicked.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
btn_180.clicked.connect(workimage.do_180)
btn_blur.clicked.connect(workimage.do_blur)
btn_contrast.clicked.connect(workimage.do_contrast)
btn_crop.clicked.connect(workimage.do_square)
app.exec()