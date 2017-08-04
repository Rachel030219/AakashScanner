# coding=utf-8

import telebot
import sqlite3

import config

bot = telebot.TeleBot(config.token)
rules = open(config.rule_db, "r")
name_rules = {}
content_rules = {}
equal_content_rules = {}


for rule in rules.readlines():
    separated_rule = rule.strip().split("|")
    if separated_rule[0] == "name":
        name_rules[separated_rule[2]] = separated_rule[1]
    if separated_rule[0] == "text":
        content_rules[separated_rule[2]] = separated_rule[1]
    if separated_rule[0] == "equal_text":
        equal_content_rules[separated_rule[2]] = separated_rule[1]


@bot.message_handler(func=lambda message: "group" in message.chat.type)
@bot.message_handler(content_types=['new_chat_members'])
def check_content(message):
    create()
    if message.new_chat_member is not None and (message.new_chat_member.username is None or "AakashScanner_bot" not in message.new_chat_member.username):
        user_id = message.new_chat_member.id
        chat_id = message.chat.id
        name = message.new_chat_member.first_name
        if message.new_chat_member.last_name is not None:
            name += " " + message.new_chat_member.last_name
        for key in name_rules.keys():
            if key.decode("utf-8") in name:
                plus_possibility(user_id, chat_id, int(name_rules[key]))
    if message.text is not None:
        user_id = message.from_user.id
        chat_id = message.chat.id
        if check_status(user_id) and read(user_id) >= 50:
            kick_user(user_id, chat_id)
        else:
            for key in content_rules.keys():
                if "," in key.decode("utf-8"):
                    keys = key.decode("utf-8").split(",")
                    match = True
                    for each in keys:
                        if each not in message.text and match:
                            match = False
                    if match:
                        plus_possibility(user_id, chat_id, int(content_rules[key]))
                else:
                    if key.decode("utf-8") in message.text:
                        plus_possibility(user_id, chat_id, int(content_rules[key]))
            for key in equal_content_rules.keys():
                if key.decode("utf-8") == message.text:
                    plus_possibility(user_id, chat_id, int(equal_content_rules[key]))


def plus_possibility(user_id, chat_id, value):
    if check_status(user_id):
        update(user_id, (int(read(user_id)) + value))
    else:
        insert(user_id, value)
    if int(read(user_id)) >= 50:
        kick_user(user_id, chat_id)


def kick_user(user_id, chat_id):
    try:
        if bot.kick_chat_member(chat_id, user_id):
            bot.send_message(chat_id, u"检测到疑似阿三 " + str(user_id) + u"\n已经自动移除")
        else:
            bot.send_message(chat_id, u"检测到疑似阿三 " + str(user_id) + u"\n但移除失败")
    except:
        bot.send_message(chat_id, u"检测到疑似阿三 " + str(user_id) + u"\n请将 bot 设置为管理员来移除，或者取消可疑对象的管理员权限")


def check_status(user_id):
    db = sqlite3.connect(config.sqlite_db)
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
    db = sqlite3.connect(config.sqlite_db)
    cursor = db.cursor()
    cursor.execute('''INSERT INTO data(id, possibility) VALUES(?,?)''', (user_id, possibility))
    db.commit()
    db.close()


def update(user_id, possibility):
    db = sqlite3.connect(config.sqlite_db)
    cursor = db.cursor()
    cursor.execute('''UPDATE data SET possibility=? WHERE id=? ''', (possibility, user_id))
    db.commit()
    db.close()


def read(user_id):
    db = sqlite3.connect(config.sqlite_db)
    cursor = db.cursor()
    cursor.execute('''SELECT possibility FROM data WHERE id=? ''', (user_id,))
    message = cursor.fetchone()[0]
    db.close()
    return message


def create():
    db = sqlite3.connect(config.sqlite_db)
    cursor = db.cursor()
    if cursor.execute('''SELECT count(*) FROM sqlite_master WHERE type=? AND name=? ''',
                      ("table", "data")).fetchone()[0] is 0:
        cursor.execute('''CREATE TABLE data(id INTEGER, possibility INTEGER)''')
        db.commit()
    db.close()


bot.polling()
