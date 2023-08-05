show = ValueError()
from requests import get as m
import vk_api
import os
import random
import re
import bot_vk
import time
def parse(s,pol=1):
    while "||" in s:
        ss= re.findall(".*\{(.*?)\|\|(.*?)\}.*",s )
        if ss == []:
            break
        boy,girl = ss[0] 
        ins= girl
        if pol !=1:
            ins =boy
        s = s.replace(r"{"+boy+r"||"+girl+r"}", ins)
    return s

def internet_on(site="https://vk.com"):
    """проверяет, включен ли интернет."""
    try:
        m(site)
        return True
    except: 
        return False
def auth_vk(token=None, login = None,password = None):
    "модуль для авторизации вконтакте."
    if internet_on() == True:
            
        if login!= None and password != None: 
            vk = vk_api.VkApi(login = login,password = password)
            vk.auth()
            return vk
        elif token!=None:
            vk = vk_api.VkApi(token = token)
            vk._auth_token()
            return vk
        elif password == None or password == "":
            raise show("НЕТ ПАРОЛЯ!!!")
        else:
            raise show("неправильные данные")
    else:
        raise show("подключение к интернету отсутствует")
def dele(file):
    """удаляет файл. ХЗ, зачем нужен, но он тут :3"""
    return os.remove(file)

def vk_bot(szenarii1,szenarii2,message_neznayu="я не знаю, как ответить(((",attachment_neznayu = "doc302808715_475715032",attachments=None,keyboard=None,vk = None,login = None,password = None,token = None):
    """
    модуль для создания чат-бота
    szenarii1 - list,в котором через запятую перечисленны варианты того, что
        пользователь может прислать(сценарии) 
    szenarii2 - list,  котором перечисленны ответы на szenarii1. ВАЖНО!!!
        Для каждого элемента szenarii1
        должен быть свой ответ. Можно использовать {firstname}, {lastname},{city} -
            будет превращено в имя, фамилию, город пользователя. Так же можно использовать {||}, который превратится в текст,
            в зависемости от пола пользователя - слева от || текст увидят мужчины, справа - женщины. Пример:
                szenarii1 = ["привет","ты кто?"]
                szenarii2 = ['Привет,{firstname} я - чат-бот, у которого есть команда "ты кто"',"теперь я просто чат-бот, а ты надеюсь, понял{||a} логику"]
    message_neznayu - str объект(сообщение), которое бот будет посылать на неизвестный сценарий.
    attachment_neznayu - str объект, attachment который бот будет посылать на неизвестный сценарий.
    
    attachments - или передавать None, или list, как и szenarii2, только для медиавложений. Если для какого-то сценария attachments отсутствует,
        то передовать пустой элемент. Пример:
            attachments = ["photo-165897409_456239349,photo-165897409_456239277",""]
    keyboard - или передавать None, или передавать list, в котором каждое значение соответствует
        клавиатуре для данного сценария. Если клавиатуры для какого-то сценария нет, то передавать bot_vk.keyboard.keyboard_none()
        
    vk - параметр bot_vk.auth_vk() Если не передан, то должн быть передан token или login и password
    login - login от вашего аккаунта вк. Передается вместе с password, если не передан vk
    password - пароль от вашего аккаунта вк. Передается вместе с логином
    token - токен группы или access token пользователя. Передается если не передан параметр vk, login, password 

    """
    if keyboard!= None:
        for i in range(len(keyboard)):
            if keyboard[i] == None:
                keyboard[i] = bot_vk.keyboard.keyboard_none()
    if keyboard==None:
            
            sinus = bot_vk.keyboard.keyboard_none()
            keyboard = [sinus]*len(szenarii1)
    if attachments == None:
            attachments = [""]*len(szenarii1)
    if internet_on() == True:
        
        if len(szenarii1) == len(szenarii2):
            
                
            """
            если параметр vk не передан, то создаем его используя логин и пароль, или токен.
            """
            if vk == None:
                if login!=None and password!=None:
                    vk = vk_api.VkApi(login = login,password = password)
                    vk.auth()
                elif token != None:
                    vk = vk_api.VkApi(token = token)
                    vk._auth_token()
                else:
                    raise show("нужен пароль с логином, или access token")

            id_own = vk.method("users.get",{})
            if id_own!=[]:
                id_own = id_own[0]["id"]
            def bot():
                info = vk.method("messages.getConversations",{"count":10})
                if info["count"]>0:
                    id = info["items"][0]["last_message"]["from_id"]
                    """проходим проверку, кто прислал сообщение, наш бот, или пользователь"""
                    if info["items"][0]["last_message"]["from_id"]>0:# and id_own != info["items"][0]["last_message"]["from_id"]:
                        
                        message = info["items"][0]["last_message"]["text"]
                        ininon = vk.method("users.get",{"user_ids":id,"fields":"id,city,sex"})[0]
                        if "city" in ininon:
                            city = ininon["city"]["title"]
                        else:
                            city = "Москва"
                        firstname = ininon["first_name"]
                        lastname =ininon["last_name"]
                        pol = ininon["sex"]
                        
                        
                        s = 1
                        for i in range(len(szenarii1)):
                            if s == 0:
                                break
                            mes =szenarii1[i]
                            if mes.lower() == message.lower():
                                s = 0
                                string = bot_vk.parse(szenarii2[i], pol).format(firstname=firstname,lastname=lastname,city=city)
                                
                                vk.method("messages.send",{"message":string.format(firstname=firstname,lastname=lastname),"user_id":id,"attachment": attachments[i],"keyboard":keyboard[i]})
                            
                        if s == 1:
                            string = bot_vk.parse(message_neznayu, pol).format(firstname=firstname,lastname=lastname,city=city)
                            vk.method("messages.send",{"message":string,"user_id":id,"attachment":attachment_neznayu})
                        
            """запускаем скрипт"""
            while True:
                try:
                    bot()
                except:
                    time.sleep(0.1)


                    
        else:
            raise show("длина массива со сценариями должна быть равна 2-му")
