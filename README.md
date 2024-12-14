## Как запустить dev
### Переход в директорию проекта:
```bash
cd 4AMVP
```
### Создание виртуального окружения:
```bash
python -m venv venv
```
### Активация виртуального окружения
```bash
venv\Scripts\activate
```
### Установка зависимостей
```bash
pip install -r requirements.txt
```
### Выполнение миграций
```bash
python manage.py migrate
```
### Создание суперюзера (для админки)
```bash
python manage.py createsuperuser
```
### Запуск
```bash
python manage.py runserver
```
