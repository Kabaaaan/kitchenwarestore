# KitchenwareStore

**KitchenwareStore** — это современное веб-приложение для управления ассортиментом и продажами кухонных товаров. Приложение разработано с использованием современных технологий: **FastAPI** для бэкенда, **Vue.js** для фронтенда и **MySQL** в качестве базы данных.

## Структура проекта

Проект разделен на две основные части:
- **backend** — серверная часть на FastAPI.
- **frontend** — клиентская часть на Vue.js.

## Установка и запуск

### 1. Установка зависимостей

Перед запуском проекта убедитесь, что у вас установлены все необходимые зависимости.

#### Бэкенд (FastAPI)
Перейдите в директорию `backend/app` и установите зависимости:

```bash
pip install -r requirements.txt
```

#### Фронтенд (Vue.js)

Перейдите в директорию frontend/kitchenware и установите зависимости:

```bash
npm install
npm install axios
npm install -D sass-embedded
```

### 2. Запуск серверной части (FastAPI)
Для запуска серверной части перейдите в директорию backend/app и выполните команду:

```bash
uvicorn main:app --reload
```

Доступ к swagger по адресу http://127.0.0.1:8000

### 3. Запуск клиентской части (Vue.js)
Для запуска клиентской части перейдите в директорию frontend/kitchenware и выполните команду:

```bash
npm run dev
```

#### 4. Использование 

http://localhost:5173


## Установка и запуск с Docker

```bash
git clone https://github.com/Kabaaaan/kitchenwarestore.git
```

```bash
cd kitchenwarestore
```

```bash
docker-compose up --build
```

Swagger - http://loaclhost:8000/docs; Vue application - http://loaclhost:8080/


## Основные функции приложения

* Просмотр каталога кухонных товаров.

* Добавление, редактирование и удаление товаров.

* Управление заказами.

* Аутентификация и авторизация пользователей.

* Поиск и фильтрация товаров.
