#  SQL STRUCTURED QUERY LANGUAGE

import sqlite3

from datetime import datetime

# создаем бот подключить
connection = sqlite3.connect('dostavka.db')
# переводчик/исполнитель
sql = connection.cursor()

# создаем запрос на создание таблицы (таблица пользователей, склад, корзина)
sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, '
            'phone_number TEXT, address TEXT, reg_date DATETIME);')

# создаем таблицу для склада
sql.execute('CREATE TABLE IF NOT EXISTS '
            'products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, '
            'pr_price REAL,pr_quantity INTEGER, pr_descr TEXT, pr_photo TEXT, '
            'reg_date DATETIME);')

# (ДЗ) создаем корзину
sql.execute('CREATE TABLE IF NOT EXISTS '
            'user_cart (user_id INTEGER, user_product TEXT, pr_quantity INTEGER, '
            'total_for_product REAL);')


# total_for_product REAL- это цена за один конкретный продукт, а не общая стоимость продукта

# Функции
def register_user(tg_id, name, phone_number, address):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    # добавляем в базу пользователя
    sql.execute('INSERT INTO users '
                '(tg_id, name, phone_number, address, reg_date) VALUES'
                '(?,?,?,?,?);', (tg_id, name, phone_number, address, datetime.now()))

    # запись обновляется
    connection.commit()


# проверка пользователя есть ли в базе
def check_user(user_id):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    checker = sql.execute('SELECT tg_id FROM users WHERE tg_id=?;', (user_id,))

    if checker.fetchone():
        return True

    else:
        return False


# (склад) добавление продукта в таблицу products
def add_product_to_sklad(pr_name, pr_count, pr_price, pr_descr, pr_photo):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()

    # добавляем в базу пользователя
    sql.execute('INSERT INTO products'
                '(pr_name, pr_price, pr_quantity, pr_descr, pr_photo, reg_date)'
                'VALUES(?,?,?,?,?,?);',
                (pr_name, pr_price, pr_count, pr_descr, pr_photo, datetime.now()))

    # запись обновляется
    connection.commit()


# удаление продуктов из склада-ДЗ
def delete_product_from_sklad(products):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()
    sql.execute('DELETE from products;', (products,))

    # запись обновляется
    connection.commit()


# удаление продукта из склада-ДЗ (pr_id)
def delete_exact_product_from_sklad(pr_id, pr_quantity):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()

    # удалить продукт из корзины через pr_id
    sql.execute('DELETE FROM sklad '
                'WHERE user_product=? AND user_id=?;', (pr_id, pr_quantity,))
    # запись обновляется
    connection.commit()


# получать все продукты из базы (name, id  )
def get_pr_name_id():
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()

    # получаем все продукты из базы (name, id)
    products = sql.execute('SELECT '
                           'pr_name, pr_id, pr_quantity FROM products').fetchall()

    print(products)

    # сортируем только те что остались на складе
    sorted_products = [(i[0], i[1]) for i in products if i[2] > 0]

    # чистый список продуктов [(name, id), (name, id) ..... (name, id)]
    return sorted_products


# создает список который состоит из продуктов
def get_pr_id():
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()

    # получаем все продукты из базы (name, id)
    products = sql.execute('SELECT '
                           'pr_name, pr_id, pr_quantity FROM products').fetchall()

    # сортируем только те что остались на складе
    sorted_products = [i[1] for i in products if i[2] > 0]

    # чистый список продуктов [(name, id), (name, id) ..... (name, id)]
    return sorted_products


# Получить информацию про определенный продукт (через pr_id) -> (photo, des, price)
def get_exact_product(pr_id):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()

    exact_product = sql.execute('SELECT pr_photo, pr_descr, pr_price '
                                'FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    return exact_product


# добавление продуктов в корзину пользователя
def add_product_to_cart(user_id, product, quantity):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')

    # переводчик/исполнитель
    sql = connection.cursor()

    # получить цену продукта из базы
    product_price = get_exact_product(product)[2]

    sql.execute('INSERT INTO user_cart '
                '(user_id, user_product, pr_quantity, total_for_product) VALUES '
                '(?,?,?,?);',
                (user_id, product, quantity, quantity * product_price))
    # сохранить изменение
    connection.commit()


# удаление продуктов из корзины
def delete_exact_product_from_cart(pr_id, user_id):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    # удалить продукт из корзины через (pr_id)
    sql.execute('DELETE FROM user_cart '
                'WHERE user_product=? AND user_id=?;', (pr_id, user_id))

    # сохранить изменение
    connection.commit()


# очищаем корзину всю
def delete_product_from_cart(user_id):
    # создаем бот подключить
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    # удалить продукт из корзины через (pr_id)
    sql.execute('DELETE FROM user_cart '
                'WHERE user_id=?;', (user_id,))

    # сохранить изменение
    connection.commit()


# вывод корзины пользователя через (user_id)
# (user_id) -> [(product, quantity, total_for_pr), (product, quantity, total_for_pr)]
def get_exact_user_cart(user_id):
    # Создаем подключения
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    user_cart = sql.execute('SELECT '
                            'products.pr_name, '
                            'user_cart.pr_quantity, '
                            'user_cart.total_for_product '
                            'FROM user_cart  '
                            'INNER JOIN products ON products.pr_id=user_cart.user_product '
                            'WHERE user_id=?;',
                            (user_id,)).fetchall()

    return user_cart


# получить номер телефона и имя пользователя

def get_user_number_name(user_id):
    # создаем подключения
    connection = sqlite3.connect('dostavka.db')
# переводчик-исполнитель
    sql = connection.cursor()
    exact_user=sql.execute('SELECT name, phone_number FROM users WHERE tg_id=?;', (user_id, ))
    return exact_user.fetchone()


