# KitchenwareStore

**KitchenwareStore** — это современное веб-приложение для управления ассортиментом и продажами кухонных товаров. Приложение разработано с использованием современных технологий: **FastAPI** для бэкенда, **Vue.js** для фронтенда и **MySQL** в качестве базы данных.

## Структура проекта

Проект разделен на две основные части:
- **backend** — серверная часть на FastAPI.
- **frontend** — клиентская часть на Vue.js.

├── backend
│   └── app
│       ├── api
│       │   ├── api_config.py        
│       │   ├── v1
│       │   │   ├── endpoints        
│       │   │   │   ├── brands.py    
│       │   │   │   ├── categories.py
│       │   │   │   ├── orders.py    
│       │   │   │   ├── products.py  
│       │   │   │   ├── users.py     
│       │   │   │   ├── __init__.py  
│       │   │   ├── routers.py       
│       │   │   ├── schemas
│       │   │   │   ├── schemas.py   
│       │   │   │   ├── __init__.py  
│       │   │   ├── __init__.py      
│       │   ├── __init__.py
│       ├── database
│       │   ├── models
│       │   │   ├── base_model.py    
│       │   │   ├── db_config.py     
│       │   │   ├── models.py        
│       │   │   ├── __init__.py      
│       │   ├── script.sql
│       │   ├── script_2.sql
│       │   ├── __init__.py
│       ├── Dockerfile
│       ├── main.py
│       ├── requirements.txt
│       ├── static
│       │   └── images
│       │       └── placeholder.png  
│       ├── utils
│       │   ├── auth.py
│       │   ├── file_utils.py        
│       │   ├── helpers.py
│       │   ├── jwt_config.py        
│       │   ├── logging.py
│       │   ├── mail.py
│       │   ├── __init__.py
│       ├── __init__.py
|
├── frontend
│   └── kitchenware
│       ├── Dockerfile
│       ├── index.html
│       ├── jsconfig.json
│       ├── nginx.conf
│       ├── package-lock.json
│       ├── package.json
│       ├── public
│       │   └── favicon.ico
│       ├── README.md
│       ├── src
│       │   ├── App.vue
│       │   ├── assets
│       │   │   ├── admin_panel.scss
│       │   │   ├── base.css
│       │   │   ├── main.css
│       │   │   ├── modal.scss
│       │   │   └── profile.css
│       │   ├── components
│       │   │   ├── AdminNav.vue
│       │   │   ├── CartItem.vue
│       │   │   ├── Order.vue
│       │   │   └── Product.vue
│       │   ├── main.js
│       │   ├── router
│       │   │   └── index.js
│       │   ├── utils
│       │   │   ├── api.js
│       │   │   ├── fetchUserDataMixin.js
│       │   │   └── refresh.js
│       │   └── views
│       │       ├── AboutView.vue
│       │       ├── admin
│       │       │   ├── BrandsView.vue
│       │       │   ├── CategoriesView.vue
│       │       │   ├── ImagesView.vue
│       │       │   └── ProductsView.vue
│       │       ├── CatalogView.vue
│       │       ├── HomeView.vue
│       │       ├── ProductView.vue
│       │       ├── ProfileView.vue
│       │       └── SignView.vue
│       └── vite.config.js
├── kitchenware.sql
├── Readme.md
└── docker-compose.yml

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

Перейти в корень приложения - /my-project;
Выполнить команду docker-compose up --build;

Swagger - http://loaclhost:8000/docs
Vue application - Swagger - http://loaclhost:8080/


## Основные функции приложения

* Просмотр каталога кухонных товаров.

* Добавление, редактирование и удаление товаров.

* Управление заказами.

* Аутентификация и авторизация пользователей.

* Поиск и фильтрация товаров.