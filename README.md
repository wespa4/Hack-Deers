<div align="center">
  
# ЦИФРОВОЙ ПРОРЫВ: СЕЗОН ИИ <br> Определение вида отходов строительства в кузове транспортного средств

<img height="300" alt="logo" src="assets/logo.jpg">

</div> 


## Оглавление
- ### [Задание](#1)
- ### [Решение](#2)
- ### [Запуск кода](#3)
- ### [Уникальность нашего решения](#4)
- ### [Стек](#5)
- ### [Команда](#6)
- ### [Ссылки](#7)

## <a name="1"> Задание </a>

В настоящее время для Департамента, как и для города в целом, одной из актуальных проблем обращения с отходами строительства является их подмена и несанкционированный сброс в непредназначенных для этого местах недобросовестными перевозчиками. Определение вида отходов в кузове самосвалов с помощью анализа видеопотока с камер видеонаблюдения и других объективных средств контроля позволит обеспечить своевременное выявление вида перевозимых отходов строительства и значительно сократить случаи подлогов, оплаты некорректных перевозок и нелегальных сбросов отходов в городе. Участникам предлагается реализовать программный модуль на основе искусственного интеллекта, который будет в состоянии проводить анализ содержимого кузова самосвала, перевозящего отходы строительства и сноса, и автоматически определять какой тип отходов он перевозит.

## <a name="2">Решение </a>

### Архетиктура решения

<div align="center">
<img height="500" alt="logo" src="assets/solution.png">

**Развертывание модели**
</div> 

### Архетиктура модели

<div align="center"><img height="300" alt="модель" src="assets/model.png"></div>

## <a name="3">Запуск кода </a>

### Последовательные шаги для запуска кода:
1. Склонируйте гит репозиторий;
```Bash
git clone https://github.com/Skadar7/Waste-detection.git
```
2. Скачайте веса для модели детекции https://drive.google.com/drive/folders/1PoQqqHhpZxaRjLQRwCxJ7xmoGyvGAyt3?usp=sharing. В ```pyClient/weights``` должны находится веса модели для статичного режима работы (рекомендовано **detr-x-10ep-3v.pt**), а в ```modelStream/weights``` – для работы в прямом эфире (рекомендовано **yolo8s_30ep.pt**).

3. Развертывание программы:
```Bash
cd Waste-detection
docker-compose build
docker-compose up
```

4. Для доступа к сайту необходимо перейти по ссылке http://localhost:4000

### Запуск инференса
```bash
cd pyClient
python3 inference.py -v {path_to_video} -hd {path_to_weights}
```
где path_to_video – путь к видео, path_to_weights – путь к весам модели

## <a name="4">Уникальность нашего решения </a>

1. Быстрая обработка видео за счет обработки наиболее информативных кадров

2. Возможность обработки в режиме реального времени с применением более быстрой модели

3. Использование докера для упрощения развертывания 

4. Автогенерация отчета в формате excel таблицы при обработке статического видео

5. Rest API для легкой интеграции в любую систему

## <a name="5">Стек </a>
<div align="center">
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pytorch/pytorch-original.svg" title="Pytorch" alt="Pytorch" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/numpy/numpy-original.svg" title="Numpy" alt="Numpy" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/opencv/opencv-original.svg" title="OpenCV" alt="OpenCV" height="40"/>&nbsp;
  
  <img src="https://pjreddie.com/media/image/yologo_2.png" title="Yolo" alt="Yolo" height="40"/>&nbsp;
  <img src="https://fuzeservers.ru/wp-content/uploads/4/7/b/47bf752c2f13d3f13363ea5b624bd2db.png" title="JS" alt="JS"  height="40"/>&nbsp;
  <img src="https://fronty.com/static/uploads/1.11-30.11/languages%20in%202022/go.png" title="GO" alt="GO" height="40"/>&nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg"  title="Flask" alt="Flask" height="40"/>
</div>

## <a name="6">Команда </a>
-
*Состав команды "Оседлавшие тильт"*   

- <h4><img align="center" height="25" src="https://user-images.githubusercontent.com/51875349/198863127-837491f2-b57f-4c75-9840-6a4b01236c7a.png">: @Ubludor, Маслов Денис - Fullstack-developer</h3>
- <h4><img align="center" height="25" src="https://user-images.githubusercontent.com/51875349/198863127-837491f2-b57f-4c75-9840-6a4b01236c7a.png">: @BuldakovN, Булдаков Никита - CV-engineer</h3>
- <h4><img align="center" height="25" src="https://user-images.githubusercontent.com/51875349/198863127-837491f2-b57f-4c75-9840-6a4b01236c7a.png">: @vseesheoleg, Сивец Олег - CV-engineer</h3>
- <h4><img align="center" height="25" src="https://user-images.githubusercontent.com/51875349/198863127-837491f2-b57f-4c75-9840-6a4b01236c7a.png">: @Skadar7, Кузнецов Денис - CV-engineer</h3>
- <h4><img align="center" height="25" src="https://user-images.githubusercontent.com/51875349/198863127-837491f2-b57f-4c75-9840-6a4b01236c7a.png">: @Llaceyne, Гулария Лана - Designer, Frontend-developer</h3>

## <a name="7">Ссылки </a>

- [ссылка на веса модели детекции](https://drive.google.com/drive/folders/1PoQqqHhpZxaRjLQRwCxJ7xmoGyvGAyt3?usp=sharing)&nbsp;
- [ссылка на скринкаст](https://drive.google.com/drive/folders/1BwoBICXg2sa_pRCZ6IFFrk211rVWjvbB?usp=sharing)&nbsp;
