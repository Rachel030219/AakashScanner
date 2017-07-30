# coding=utf-8

import telebot
import sqlite3

bot = telebot.TeleBot("<TOKEN>")


@bot.message_handler(func=lambda message: "group" in message.chat.type)
def check_content(message):
    create()
    if message.new_chat_member is not None and\
            (message.new_chat_member.username is None or "AakashScanner_bot" not in message.new_chat_member.username):
        create()
        user_id = message.new_chat_member.id
        chat_id = message.chat.id
        if message.new_chat_member.username is not None and "Aakash" in message.new_chat_member.username:
            plus_possibility(user_id, chat_id, 10)
        if "Aakash" in message.new_chat_member.first_name:
            plus_possibility(user_id, chat_id, 5)
        if message.new_chat_member.last_name is not None and u"🇮🇳" in message.new_chat_member.last_name:
            plus_possibility(user_id, chat_id, 10)
    if message.text is not None:
        user_id = message.from_user.id
        chat_id = message.chat.id
        if check_status(user_id) and read(user_id) >= 50:
            kick_user(user_id, chat_id)
        else:
            if u"如果你给前总统一秒钟，他会很开心" in message.text:
                plus_possibility(user_id, chat_id, 15)
            if u"+1s" == message.text:
                plus_possibility(user_id, chat_id, 5)
            if u"666" in message.text and u"233" in message.text:
                plus_possibility(user_id, chat_id, 15)
            if u"China" in message.text and u"president" in message.text:
                plus_possibility(user_id, chat_id, 10)


def plus_possibility(user_id, chat_id, value):
    if check_status(user_id):
        update(user_id, (int(read(user_id)) + value))
    else:
        insert(user_id, value)
    if int(read(user_id)) >= 50:
        kick_user(user_id, chat_id)


def kick_user(user_id, chat_id):
    if bot.kick_chat_member(chat_id, user_id):
        bot.send_message(chat_id, u"检测到疑似阿三 " + str(user_id) + u"\n已经自动移除")
    else:
        bot.send_message(chat_id, u"检测到疑似阿三 " + str(user_id) + u"\n请将 bot 设置为管理员来移除")


def check_status(user_id):
    db = sqlite3.connect('/home/rachel/Bot/data/aakashscanner.db')
    create()
    cursor = db.cursor()
    cursor.execute('''SELECT id FROM data''')

    for row in cursor.fetchall():
        if user_id == row[0]:
            db.close()
            return True
    db.close()
    return False


def insert(user_id, possibility):
    db = sqlite3.connect('/home/rachel/Bot/data/aakashscanner.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO data(id, possibility) VALUES(?,?)''', (user_id, possibility))
    db.commit()
    db.close()


def update(user_id, possibility):
    db = sqlite3.connect('/home/rachel/Bot/data/aakashscanner.db')
    cursor = db.cursor()
    cursor.execute('''UPDATE data SET possibility=? WHERE id=? ''', (possibility, user_id))
    db.commit()
    db.close()


def read(user_id):
    db = sqlite3.connect('/home/rachel/Bot/data/aakashscanner.db')
    cursor = db.cursor()
    cursor.execute('''SELECT possibility FROM data WHERE id=? ''', (user_id,))
    message = cursor.fetchone()[0]
    db.close()
    return message


def create():
    db = sqlite3.connect('/home/rachel/Bot/data/aakashscanner.db')
    cursor = db.cursor()
    if cursor.execute('''SELECT count(*) FROM sqlite_master WHERE type=? AND name=? ''',
                      ("table", "data")).fetchone()[0] is 0:
        cursor.execute('''CREATE TABLE data(id INTEGER, possibility INTEGER)''')
        db.commit()
    db.close()


bot.polling()
