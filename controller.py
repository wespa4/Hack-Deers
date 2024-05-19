import datetime
import os
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import matplotlib.pyplot as plt
from ultralytics import RTDETR,YOLO
import shutil
import seaborn as sns
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

path = "./_internal/"
path = ""



class App(QMainWindow):
    def __init__(self,model):
        super().__init__()
        uic.loadUi(path+"gui.ui",self)

        
        self.label.setPixmap(QPixmap(path+"gerb.png"))
        

        self.model = model

        self.strart_b.clicked.connect(self.start)
        self.select_path.clicked.connect(self.setPathToSource)
        self.path_line.textChanged.connect(self.setCountAll)

        self.listFiles = []
        self.animals = ['Кабарга', 'Косуля', 'Олень']
        self.animalsDict = {'0':'Кабарга', '1':'Косуля', '2':'Олень'}
        self.folder_name = ""
        self.ratio = [0,0,0]

    
    def start(self):
        
        if self.info.text() == "Такая папка есть":
            print("start")
            self.startClassification()
            self.Kab.display(self.ratio[0])
            self.Kos.display(self.ratio[1])
            self.Ole.display(self.ratio[2])
            if self.b_grafic.isChecked():
                self.showGistagramma()
        else:
            self.info.setText("Путь к папке с ошибкой")
            print("Не соблюдены условия")
    

    
    def startClassification(self):
        
        fin_dict = {}
        i = 0
        self.ratio = [0,0,0]
        for elem in self.listFiles:
            i += 1
            print("Обрабатывается картика номе: "+str(i))
            path = self.path_line.text()+"/"+elem
            
            #time.sleep(0.1)
            #модель
            yres = self.YoloClassification(path = path)
            print(yres)
            self.ratio[int(yres)] += 1 
            fin_dict[path] = self.animalsDict[yres]
            #логика после модели
        #print("-------------------------------------------------------------------------------------------------")
        print(fin_dict)
        

        all_classes = {}
        for pth in fin_dict:
            class_animal = fin_dict[pth]
            all_classes[class_animal] = True
        #создание папок
        folder_name = self.createFolderForClasses(fin_dict,all_classes)
        print(folder_name)
        #сортировка
        for pth in fin_dict:
            #print("copy "+pth+" -> "+os.path.join(self.folder_name, fin_dict[pth]))
            shutil.copy2(pth, os.path.join(self.folder_name, fin_dict[pth]))
            
        shutil.make_archive(self.folder_name, 'zip', folder_name)
        shutil.rmtree(folder_name)

    def createFolderForClasses(self,f_dict,all_classes):
        #создание папок
        now = datetime.datetime.now()
        date_time = now.strftime("%H.%M.%S")
        # Создаем название папки
        index = self.path_line.text().rfind('/')
        result = self.path_line.text()[index+1:]
        self.folder_name = result+"_"+date_time

        # Создаем новую папку в рабочей директории
        os.makedirs(self.folder_name)

        for cls in all_classes:
            folder_path = os.path.join(self.folder_name, cls)
            print(folder_path)
            os.makedirs(folder_path)

        return self.folder_name


    def YoloClassification(self,path):
        
        results = self.model(path) # путь к данным
        names = self.model.names  # все классы модели
        result_names = None  # результаты

        for i, res in enumerate(results):
            boxes = res.boxes.cpu().numpy()
            #print("Обрабатывается картинка по счету",i)
            for box in boxes:
                result_names = names[int(box.cls)] 
                break
        if result_names:
            return result_names
        else:
            return result_names
            



    def showGistagramma(self):
        
        # # counts = [5, 10, 15]  # Замените это значение на реальные данные

        # plt.bar(self.animals, self.ratio, color=['blue', 'green', 'orange', 'red'])
        # plt.ylabel('Количество')
        # plt.title('Гистограмма встреченных оленевидных')

        # plt.show()
        self.plot_histogram(self.ratio, self.animals)

    def plot_histogram(self,file_counts, directories):
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        # Используем гистограмму с осями в обратном порядке для удобства чтения
        ax = sns.barplot(x=directories, y=file_counts, palette="viridis")
        ax.set_title('Количество фотографий')
        plt.show()
        

    def setPathToSource(self):
        dialog = QFileDialog()
        file = dialog.getExistingDirectory(None, "Select Folder")
        #print(file)
        self.path_line.setText(file)
        
        
    def setCountAll(self):
        directory = self.path_line.text()
        
        try:
            files = os.listdir(directory)
            
            self.info.setText("Такая папка есть")
            files = [file for file in files if file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".JPG")]

            self.listFiles = files

            self.All.display(len(files))
        except:
            self.info.setText("Такой папки нет")
            self.All.display(-1)
            self.listFiles = []
            


if __name__ == '__main__':
    print("init gui")
    
    app = QApplication(sys.argv)
    print("init model")
    
    #model = YOLO(path+'yolov8n.pt')
    model = YOLO(path+'yolov9e_20ep_1024sz_v6.pt')
    #model = RTDETR(path+'last.pt')
    #model.to('cuda')
    print("inited all")
    
    
    try:
        ex = App(model=model)
        print("show window")
        
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)