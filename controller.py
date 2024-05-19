import datetime
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import matplotlib.pyplot as plt
from ultralytics import YOLO
import shutil
import seaborn as sns
import os
import torch
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
            yres = self.YoloClassification(path = path)
            print(yres)
            self.ratio[int(yres)] += 1 
            fin_dict[path] = self.animalsDict[yres]
        print(fin_dict)


        all_classes = {}
        for pth in fin_dict:
            class_animal = fin_dict[pth]
            all_classes[class_animal] = True
        folder_name = self.createFolderForClasses(fin_dict,all_classes)
        print(folder_name)
        for pth in fin_dict:
            shutil.copy2(pth, os.path.join(self.folder_name, fin_dict[pth]))
            
        shutil.make_archive(self.folder_name, 'zip', folder_name)
        shutil.rmtree(folder_name)

    def createFolderForClasses(self,f_dict,all_classes):
        now = datetime.datetime.now()
        date_time = now.strftime("%H.%M.%S")
        index = self.path_line.text().rfind('/')
        result = self.path_line.text()[index+1:]
        self.folder_name = result+"_"+date_time
        os.makedirs(self.folder_name)

        for cls in all_classes:
            folder_path = os.path.join(self.folder_name, cls)
            print(folder_path)
            os.makedirs(folder_path)
        return self.folder_name


    def YoloClassification(self,path):
        results = self.model(path)
        names = self.model.names
        result_names = None

        result_names = {}
        for _, res in enumerate(results):
            boxes = res.boxes.cpu().numpy()
            for box in boxes:
                if names[int(box.cls)] not in result_names:
                    result_names[names[int(box.cls)]] = [box.conf[0]]
                else:
                    result_names[names[int(box.cls)]].append(box.conf[0])
            # Структура {Класс: [conf/conf, conf...]}
            # Если есть хотя бы что-то
            if result_names.keys():
                # Вытягиевам все объекты в 1 массив
                all_values = []
                for value in result_names.values():
                    all_values.extend(value)
                max_conf = max(all_values)
                # Если всего 1 объект
                if len(all_values) == 1:
                    return list(result_names.keys())[0]
                # Если объектов от 2 до 5
                elif 1 < len(all_values) < 5:
                    # Проходимся по всем классам
                    for i in result_names.keys():
                        # Если макс conf в этом классе, то записываем его
                        if max_conf in result_names[i]:
                            return i
                else:
                    # Если объектов больше 5
                    # Если есть олень и его conf > 0.35, то олень
                    if '2' in list(result_names.keys()) and max(result_names['2']) > 0.35:
                        return 2
                    else:
                        # Если оленя нет
                        # Проходимся по всем классам
                        for i in result_names.keys():
                            # Если макс conf в этом классе, то записываем его
                            if max_conf in result_names[i]:
                                return i
            else:
                # Если ничего не нашел записываем косулю
                return 1


    def showGistagramma(self):
        self.plot_histogram(self.ratio, self.animals)


    def plot_histogram(self,file_counts, directories):
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=directories, y=file_counts, palette="viridis")
        ax.set_title('Количество фотографий')
        plt.show()
        

    def setPathToSource(self):
        dialog = QFileDialog()
        file = dialog.getExistingDirectory(None, "Select Folder")
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
    app = QApplication(sys.argv)
    model = YOLO(path+'yolov9e_20ep_1024sz_v6.pt')
    if torch.cuda.is_available():
        model.to('cuda')
    try:
        ex = App(model=model)
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
