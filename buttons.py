import database
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton



# кнопки со всеми продуктами (основное меню)
def main_menu_kb(products_from_db):
# создаем пространство для кнопок
    kb = InlineKeyboardMarkup(row_width=2)
    order = InlineKeyboardButton(text='оформить заказ', callback_data='order')
    cart = InlineKeyboardButton(text='корзина', callback_data='cart')

# генерация кнопок с товарами (берем из базы)


# создаем кнопки с продуктами
    all_products = [InlineKeyboardButton(text=i[0], callback_data=i[1]) for i in products_from_db]
    print(all_products)

# объединить пространство с кнопками
    kb.row(order)
    kb.add(*all_products)
    kb.row(cart)
    # возвращаем кнопки
    return kb

# кнопки для выбора количества
def choose_product_count(plus_or_minus='', current_amount=1):
# создаем пространство для кнопок
    kb = InlineKeyboardMarkup(row_width=3)

# несгораемая кнопка
    back = InlineKeyboardButton(text='назад', callback_data='back')
    plus = InlineKeyboardButton(text='+', callback_data='increment')
    minus = InlineKeyboardButton(text='-', callback_data='decrement')
    count = InlineKeyboardButton(text=str(current_amount), callback_data=str(current_amount))
    add_to_cart = InlineKeyboardButton(text='добавить в корзину', callback_data='to_cart')

#     отслеживаем плюс или минус
    if plus_or_minus == 'increment':
        new_amount = int(current_amount) +1

        count = InlineKeyboardButton(text=str(new_amount),
                                     callback_data=str(new_amount))

    elif plus_or_minus == 'decrement':
        if int(current_amount) != 1:
            new_amount = int(current_amount) -1

            count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))


# объединим кнопки с пространством
    kb.add(minus, count, plus)
    kb.row(add_to_cart)
    kb.row(back)

# возвращаем кнопки
    return kb
# кнопка для отправки номера телефона
def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    number = KeyboardButton('Поделиться контактом', request_contact=True)

    kb.add(number)

    return kb

def location_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    location = KeyboardButton('Отправить локацию', request_location=True)

    kb.add(location)

    return kb


# копки для подтверждения заказа
def get_accept_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')

    kb.add(yes, no)

    return kb

# кнопки при переходе в корзину
def get_cart_kb():
    kb = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton('очистить корзину', callback_data='clear_cart')
    order = InlineKeyboardButton('оформить заказ ', callback_data='order')
    back = InlineKeyboardButton('назад ', callback_data='back')


    kb.add(clear_cart, order, back)

    return kb






