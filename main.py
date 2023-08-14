import database

import buttons

import telebot

from telebot.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim

# работает для удаления нижних кнопок в телеграме
from telebot.types import ReplyKeyboardRemove

# создаем подключение к боту и добавляем токен
bot = telebot.TeleBot('5949011183:AAEzxV9s1Cs1Lf269eAWs1N2F2829WgDPiY')

# копируем данную ссылку через поиск в Google "my user agent"
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

# словарь для временных данных
users = {}


# database.add_product_to_sklad('яблоки',
#                               12,12000,
#                               'супер самый лучший',
#                               'https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.applesfromny.com%2Fwp-content%2Fuploads%2F2020%2F05%2F20Ounce_NYAS-Apples2.png&tbnid=ktcxvF5LaXyVXM&vet=12ahUKEwiYvfm9oZP_AhWOsyoKHRz8CMwQMygBegUIARDlAQ..i&imgrefurl=https%3A%2F%2Fwww.applesfromny.com%2Fvarieties%2F&docid=C0ERe9pIHvHfgM&w=2400&h=1889&q=apple&ved=2ahUKEwiYvfm9oZP_AhWOsyoKHRz8CMwQMygBegUIARDlAQ')


@bot.message_handler(commands=['start'])
def start_message(message):
    # получить телеграм ади
    user_id = message.from_user.id
    print(user_id)
    # проверка пользователя
    checker = database.check_user(user_id)

    # если пользователь есть в базе
    if checker:
        # получить актуальный список продукта
        products = database.get_pr_name_id()
        # отправляем сообщение с меню
        bot.send_message(user_id, 'Привет ',
                         reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'выберите пункт меню ',
                         reply_markup=buttons.main_menu_kb(products))
    # если нет пользователя в базе
    elif not checker:
        bot.send_message(user_id, 'привет\n отправь свое имя')

        # переход на этап получение имени
        bot.register_next_step_handler(message, get_name)

        # получение имени


@bot.message_handler(content_types=['text'])
# Этап получения имени
def get_name(message, ):
    # Получим telegram id текущего пользователя(кто общается с ботом)
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Отправь номер', reply_markup=buttons.phone_number_kb())
    bot.register_next_step_handler(message, get_number, name)


# Этап получение номера телефона
def get_number(message, name):
    user_id = message.from_user.id

    phone_number = message.contact.phone_number
    database.register_user(user_id, name, phone_number, 'Not yet')
    products = database.get_pr_name_id()
    bot.send_message(user_id, 'вы успешно зарегистрированы ',
                     reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, 'Выбрать Меню', reply_markup=buttons.main_menu_kb(products))


# обработчик кнопок (оформить заказ,корзина)
@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'clear_cart'])
def main_menu_handler(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    #     если нажал на кнопку: оформить заказ
    if call.data == 'order':
        # удалим сообщение с верхними кнопками
        bot.delete_message(user_id, message_id)
        #     отправим текст на "отправьте локацию"
        bot.send_message(user_id,
                         'оправьте локацию',
                         reply_markup=buttons.location_kb())
        # переход на этап сохранения локации
        bot.register_next_step_handler(call.message, get_location)
    # если нажал на кнопку корзина
    elif call.data == 'cart':
# получим корзину пользователя
        user_cart = database.get_exact_user_cart(user_id)

# формируем сообщение со всеми данными
        full_text = 'ваш корзина: \n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

# итог
        full_text += f'\nИтог: {total_amount}'

#отправляем ответ пользователю
        bot.edit_message_text(full_text,
                              user_id,
                              message_id,
                              reply_markup=buttons.get_cart_kb())
# если нажал на очистить корзину
    elif call.data == 'clear_cart':
# вызов функции очистки корзины
        database.delete_product_from_cart(user_id)

# оправим ответ
        bot.edit_message_text('ваша корзина очищена',
                              user_id,
                              message_id,
                              reply_markup=buttons.main_menu_kb(database.get_pr_name_id()))



# обработчик выбора количества
@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def get_user_product_count(call):
    user_id = call.message.chat.id

    if call.data == 'increment':
        actual_count = users[user_id]['pr_count']

        users[user_id]['pr_count'] += 1
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('increment', actual_count))

    elif call.data == 'decrement':
        actual_count = users[user_id]['pr_count']

        users[user_id]['pr_count'] -= 1
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('decrement', actual_count))

    elif call.data == 'back':
        # обнуляем

        users[user_id]['pr_count'] = 0

        products = database.get_pr_name_id()

        bot.edit_message_text('выберите пункт меню ', user_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu_kb(products))

    elif call.data == 'to_cart':
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']

        database.add_product_to_cart(user_id, user_product, product_count)

        products = database.get_pr_name_id()
        bot.edit_message_text('продукт добавлен в корзину\n чо-нибудь еще ?,',
                              user_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu_kb(products))


# обработчик выбора товара
# взывает по айди продукт
@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_id())
def get_user_product(call):
    print(call)

    # сохраним айди пользователя
    user_id = call.message.chat.id
    # сохрани продукт во временный словарь
    # call.data-значение нажатой кнопки (инлайн)
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}

    # сохраним айди сообщения
    message_id = call.message.message_id

    # поменять кнопки на выбор
    bot.edit_message_text('выберите количество',
                          chat_id=user_id,
                          message_id=message_id,
                          reply_markup=buttons.choose_product_count())


def get_location(message):
    user_id = message.from_user.id

    # оправил ли локацию пользователь
    if message.location:
        # сохранить в переменные координаты
        latitude = message.location.latitude
        longitude = message.location.longitude

        # преобразуем координаты на нормальный адрес
        address = 'geolocator.reverse((latitude, longitude)).address'

        # запросить подтверждение
        # получим корзину пользователя
        user_cart = database.get_exact_user_cart(user_id)

        # формируем сообщение со всеми данными
        full_text = 'ваш заказ: \n\n'
        user_info = database.get_user_number_name(user_id)
        full_text += f'имя: {user_info[0]}\nномер телефона: {user_info[1]}\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]
        # итог и адрес
        full_text += f'\nИтог: {total_amount}\nадрес: {address}'

        bot.send_message(user_id, full_text, reply_markup=buttons.get_accept_kb())

        # преходим на этап подтверждения
        bot.register_next_step_handler(message, get_accept, address, full_text)


# функция сохранения статуса заказа
def get_accept(message, address, full_text):
    user_id = message.from_user.id

    message_id = message.message_id
    user_answer = message.text
    # получаем все продукты из базы для кнопок
    products = database.get_pr_name_id()

    if user_answer == 'Подтвердить':
# очистить корзину пользователя
        database.delete_product_from_cart(user_id)
# отправим админу сообщение о новом заказе
        bot.send_message(79088303, full_text.replace('ваш', 'новый'))

# отправить ответ
        bot.send_message(user_id, 'Возвращаемся в меню', reply_markup=ReplyKeyboardRemove())

# обратно в меню
        bot.send_message(user_id, 'Ваш заказ обрабатывается'
                         , reply_markup=buttons.main_menu_kb(products))

    elif user_answer == 'Отменить':

        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'Возвращаемся в меню', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню'
                         , reply_markup=buttons.main_menu_kb(products))


bot.polling(none_stop=True)
