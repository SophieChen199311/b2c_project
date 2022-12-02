# b2c_project
## Showdoc:
    [url](https:/www.showdoc.com.cn/2142669133683109/9625769946425766)
    pwd: 123

## Env setup:
    conda env create -f environment.yaml
    mysql:
        a.create a database to store the goods data
        b.edit the mysql info in settings.py
    redis:
        a.set on redis database to store cart data
        b.edit the redis info in settings.py
        the user's cart data would be stored like "cart_userId:{goodsId: number}"
    orm:
        run the cmd: python manage.py makemigrations
                     python manage.py migrate
        put mock goods data in mysql:
            a. cd to the location where app goods is
            b. run the cmd: python ../manage.py loaddata goods.json

## Put goods in cart(this part would be shown in detail on showdoc)
    url: 127.0.0.1:8000/cart/cart_detail
    method: Post
    request body(data): {"user_id":2, "goods_id_lst": [1,2,3,4,6]}

## Get goods and calculate the fees(this part would be shown in detail on showdoc)
    url: 127.0.0.1:8000/cart/cart_detail?user_id=2
    method:Get

## Unittest
    * Normally speaking, we would set a test database for unittest so that our data on dev database
      wouldn't be affected, but it's not applicable here as we have to get data from mysql and
      put it to redis
    The unittest file is on app cart(b2c_backend/cart/tests.py)
    run the cmd: python manage.py test

