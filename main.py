from pyrogram import Client, Filters
from pyrogram.client.types import Message

import re

from time import sleep

import json

from data import config


carts = []
with open('carts.json', 'r') as fp:
    cards_to_parse = json.load(fp)
    start = cards_to_parse['start']
    end = cards_to_parse['end']

for number_of_card in range(int(start), int(end) + 1):
    carts.append('0' * (int(len(start) - len(str(number_of_card)))) + str(number_of_card))


bot = Client('session', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)


@bot.on_message(Filters.regex('Авторизоваться') | Filters.regex('Активировать карту'))
def authorization(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            for keyboard in message.reply_markup['keyboard']:
                if 'Авторизоваться' in keyboard[0]:
                    client.send_message('VkusVillBot', keyboard[0])


@bot.on_message(Filters.regex('Политикой'))
def send_cart(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        client.send_contact('VkusVillBot', config.NUMBER, config.NAME)
        sleep(2.5)
        try:
            client.send_message('VkusVillBot', carts[0])  # берёт первую карту
            carts.remove(carts[0])  # удаляет первую взятую карту
        except IndexError:
            print('Номера карт закончились')
            return
            
        with open('carts.json', 'w') as fp:
            json.dump({'start': carts[0], 'end': carts[-1]}, fp, indent=4)


@bot.on_message(Filters.regex('Неправильный формат номера') | Filters.regex('уже привязана'))
def restart(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        client.send_message('VkusVillBot', '/start')


@bot.on_message(Filters.regex('Изменить номер телефона') | Filters.regex('я не могу определить'))
def cant_find(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        sleep(2.5)
        try:
            client.send_message('VkusVillBot', carts[0])  # берёт первую карту
            carts.remove(carts[0])  # удаляет первую взятую карту
        except IndexError:
            print('Номера закончились')
            return
        
        with open('carts.json', 'w') as fp:
            json.dump({'start': carts[0], 'end': carts[-1]}, fp, indent=4)


@bot.on_message(Filters.regex('нашли вашу карту'))
def confirm_cart(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            if message.reply_markup.inline_keyboard:
                client.request_callback_answer(
                    'VkusVillBot', message.message_id, message.reply_markup['inline_keyboard'][0][0]['callback_data']
                )


@bot.on_message(Filters.regex('обращаться'))
def send_name(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        client.send_message('VkusVillBot', config.NAME)


@bot.on_message(Filters.regex('Проблема с регистрацией'))
def send_name(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        client.send_message('VkusVillBot', '/start')


@bot.on_message(Filters.regex('всю информацию'))
def get_cart_info(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            for keyboard in message.reply_markup['keyboard']:
                if 'Карта ' in keyboard[0]:
                    client.send_message('VkusVillBot', keyboard[0])


@bot.on_message(Filters.regex('Cумма бонусов'))
def save_balance(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        cart = re.findall(r'[\d]+\.', message.text)[0].replace('.', '')

        balance = re.findall(r'[\d]+,[\d]+\.', message.text)
        
        if not balance:
            balance = '0;'
        elif balance:
            balance = balance[0].replace('.', ';')
        with open('results.txt', 'a') as f:
            f.write(cart + ': ' + balance + '\n')

        client.send_message('VkusVillBot', 'Открепить карту')
        sleep(1)


@bot.on_message(Filters.regex('открепить карту'))
def delete_cart(client: Client, message: Message) -> None:
    if message.chat.username == 'VkusVillBot':
        if message.reply_markup:
            if message.reply_markup.inline_keyboard:
                client.request_callback_answer(
                    'VkusVillBot', message.message_id, message.reply_markup['inline_keyboard'][0][0]['callback_data']
                )


bot.run()
