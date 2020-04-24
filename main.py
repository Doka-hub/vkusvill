from pyrogram import Client, Filters
import settings
import re
import time
import json
global last


carts = []
with open('carts.json', 'r') as fp:
    carts_ = json.load(fp)
for i in range(int(carts_['start']), int(carts_['end'])+1):
    if carts_['start'].startswith('0'):
        carts.append('0'+str(i))
with open('api.json') as f:
    api = json.load(f)

cl = Client('Session', api_id=api['api_id'], api_hash=api['api_hash'])


@cl.on_message(Filters.regex('Авторизоваться') | Filters.regex('Активировать карту'))
def authorization(client, message):
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            for i in message.reply_markup['keyboard']:
                if 'Авторизоваться' in i[0]:
                    client.send_message(
                        'VkusVillBot',
                        i[0]
                    )


@cl.on_message(Filters.regex('Политикой'))
def send_cart(client, message):
    if message.chat.username == 'VkusVillBot':
        client.send_contact(
            'VkusVillBot',
            settings.NUMBER,
            settings.NAME
        )
        time.sleep(2.5)
        try:
            client.send_message(
                'VkusVillBot',
                carts[0]
            )
        except IndexError:
            print('Номера карт закончились')
        carts.remove(carts[0])
        with open('carts.json', 'w') as fp:
            json.dump({
                'start': carts[0],
                'end': carts[-1]
            }, fp, indent=4)


@cl.on_message(
    Filters.regex('Неправильный формат номера') |
    Filters.regex('уже привязана')
)
def restart(client, message):
    if message.chat.username == 'VkusVillBot':
        client.send_message(
            'VkusVillBot',
            '/start'
        )


@cl.on_message(
    Filters.regex('Изменить номер телефона') |
    Filters.regex('я не могу определить')
)
def cant_find(client, message):
    if message.chat.username == 'VkusVillBot':
        time.sleep(2.5)
        try:
            client.send_message(
                'VkusVillBot',
                carts[0]
            )
        except IndexError:
            print('Номера закончились')
        carts.remove(carts[0])
        with open('carts.json', 'w') as fp:
            json.dump({
                'start': carts[0],
                'end': carts[-1]
            }, fp, indent=4)


@cl.on_message(Filters.regex('нашли вашу карту'))
def confirm_cart(client, message):
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            if message.reply_markup.inline_keyboard:
                client.request_callback_answer(
                    'VkusVillBot',
                    message.message_id,
                    message.reply_markup['inline_keyboard'][0][0]['callback_data']
                )


@cl.on_message(Filters.regex('обращаться'))
def send_name(client, message):
    if message.chat.username == 'VkusVillBot':
        client.send_message(
            'VkusVillBot',
            settings.NAME
        )


@cl.on_message(Filters.regex('Проблема с регистрацией'))
def send_name(client, message):
    if message.chat.username == 'VkusVillBot':
        client.send_message(
            'VkusVillBot',
            '/start'
        )


@cl.on_message(Filters.regex('всю информацию'))
def get_cart_info(client, message):
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            for i in message.reply_markup['keyboard']:
                if 'Карта ' in i[0]:
                    client.send_message(
                        'VkusVillBot',
                        i[0]
                    )


@cl.on_message(Filters.regex('Cумма бонусов'))
def save_balance(client, message):
    if message.chat.username == 'VkusVillBot':
        cart = re.findall(
            r'[\d]+\.',
            message.text
        )[0].replace('.', '')

        balance = re.findall(
            r'[\d]+,[\d]+\.',
            message.text
        )
        if not balance:
            balance = '0;'
        elif balance:
            balance = balance[0].replace('.', ';')
        with open('results.txt', 'a') as f:
            f.write(cart + ': ' + balance + '\n')

        client.send_message(
            'VkusVillBot',
            'Открепить карту'
        )
        time.sleep(1)


@cl.on_message(Filters.regex('открепить карту'))
def delete_cart(client, message):
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            if message.reply_markup.inline_keyboard:
                client.request_callback_answer(
                    'VkusVillBot',
                    message.message_id,
                    message.reply_markup['inline_keyboard'][0][0]['callback_data']
                )


cl.run()
