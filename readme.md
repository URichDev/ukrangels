Программа для парсинга товаров с сайта http://ukrainian-angels.com.ua/
и подготовки файла для импорта товаров в Wordpress

Описание:
-
Инструменты:
- Python==3.8
- Scrapy==2.0

**angels_export** - проект на scrapy для парсинга товаров

#### Установка:
1) Склонировать репозиторий
`git clone https://github.com/URichDev/ukrangels.git` 
2) Установит все необходимые модули, вызвав команду в командной строке:
`pip install -r requirements.txt`

#### Запуск парсера:
1) Перейти в папку angels_export с помощью команды:
`cd angels_export`
2) Запустить паука командой в командной строке: `scrapy crawl ukr_angels_spider -o outputfile.csv
`
Парсер сгенерирует файл outputfile.csv для импорта в Wordpress

#### Импорт в Wordpress
1) Должен быть установлен **Wordpress** + **Woocommerce**
2) В админ панели Wordpress зайти на вкладку **Товары** и наэать на кнопку **Начать импорт** - https://prnt.sc/rocq6y
3) Выбрать файл outputfile.csv и нажать кнопку **Продолжить** - https://prnt.sc/rocrom
4) Проверить соответствие полей и нажать кнопку **Запустить инструмент импорта**
5) Начнется процесс импорта, по окончанию все товары добавятся в базу Wordpress