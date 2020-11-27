# Yamdb
Социальная сеть для блогеров (выполнен во время обучения в Яндекс.Практикум)

# Инструкция по развертыванию проекта
1. Скачать проект или клонировать с помощью git 
```
git clone https://github.com/Caterina-Plewako/infra_sp2.git
```

2. Перейти в каталог с проектом и создать виртуальное окружение 
```
python -m venv venv
```

3. Запустить виртуальное окружение:

Для Mac/Linux:
```
source venv/bin/activate
```

Для Windows:
```
source venv/Scripts/activate
```

4. Установить все необходимые пакеты, указанные в файле requirements.txt 
```
pip install -r requirements.txt
```

5. Запустить миграции 
```
python manage.py migrate
```

6. Для проверки работы проекта запустить тестовый сервер 
```
python manage.py runserver
```

7. Перейти по адресу http://127.0.0.1:8000

# Для работы с админкой Django:
1. Создать суперпользователя 
```
python manage.py createsuperuser
```
2. Перейти по адресу http://127.0.0.1:8000/admin и ввести логин и пароль суперпользователя

# Технологии 
* Python
* Django
* SQLite
