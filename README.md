# b2c_project

## Showdoc:
* [url](https://www.showdoc.com.cn/2142669133683109/9625769946425766)
* pwd: 123

## Env setup:
* conda env create -f environment.yaml
* mysql:
  * create a database to store the goods data
  * edit the mysql info in settings.py
* redis:
  * set on redis database to store cart data
  * edit the redis info in settings.py
  * the user's cart data would be stored like "cart_userId:{goodsId: number}"
* orm:
  * run the cmd: 
    * python manage.py makemigrations
    * python manage.py migrate
  * put mock goods data in mysql:
    * cd to the location where app goods is
    * run the cmd: python ../manage.py loaddata goods.json

## Put goods in cart(this part would be shown in detail on showdoc)
* 127.0.0.1:8000/cart/cart_detail
* method: Post
* request body(data): {"user_id":2, "goods_id_lst": [1,2,3,4,6]}

## Get goods and calculate the fees(this part would be shown in detail on showdoc)
* url: 127.0.0.1:8000/cart/cart_detail?user_id=2
* method:Get

## Unittest
Normally speaking, we would set a test database for unittest so that our data on dev database
wouldn't be affected, but it's not applicable here as we have to get data from mysql and
put it to redis
* The unittest file is on app cart(b2c_backend/cart/tests.py)
* run the cmd: python manage.py test

## Hierarchy
```bash
.
├── README.md
├── b2c_backend
│   ├── __init__.py
│   ├── __pycache__
│   ├── apps
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── utils
│   └── wsgi.py
├── cart
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── service.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── environment.yaml
├── goods
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── goods.json
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── logs
│   └── b2c_project.log
├── manage.py
└── utils
    ├── __pycache__
    ├── constants.py
    └── exceptions.py
```
## Further explanation about some important folders of the project
* main apps
  * goods
  * carts
* utils
  * exceptions.py contains self-defined exceptions generic
  * constants.py contains constants we would use in the project  e.g.SHIPPING_RATE = {"US":2, "UK":3, "CN": 2}
