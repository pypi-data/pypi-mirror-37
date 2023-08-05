
import bot_vk
data = [None]
import requests
from datetime import datetime
def unixtime_converter(time):
    
    return (datetime.utcfromtimestamp(int(time+10800))).strftime('%Y-%m-%d %H:%M:%S')
def compucter_opredeli(num):
    if num == 1:
        return "mobile"
    elif num == 2:
        return "iphone"
    elif num == 7:
        return "web"
    elif num == 6:
        return "windows"
    elif num == 5:
        return "wphone"
    elif num == 3:
        return "ipad"
    elif num == 4:
        return "android"
def message_flag(flag):
    if flag == 128:
        return "message_delete"
    elif flag == 1:
        return "message_unread"
    elif flag == 2:
        return "message_fromMe"
    elif flag == 4:
        return "message_newAnswer"
    elif flag == 65536:
        return "group_whant_to_message_you"
    elif flag == 8:
        return "import_message"
    elif flag == 16:
        return "new_chatMessage"
    elif flag == 32:
        return "message_Fromfriend"
    elif flag == 64:
        return "spam_message"
    elif flag == 131072:
        return "message_deletedForAll"
    else:
        return "not_definded"
class longpoll():

    def user_longpoll(vk):
        
        """модуль для облегчения жизни и использования longpoll_api"""
        if data[0]== None:
            data[0] = vk.method("messages.getLongPollServer",{})
        try:
            dfyi = True
            response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=data[0]['server'], key=data[0]['key'], ts=data[0]['ts'])).json()  # отправление запроса на Long Poll сервер со временем ожидания 20 и опциями ответа 2
            updates = response['updates']
        except:
            dfyi = False
            data[0] = vk.method("messages.getLongPollServer",{})
        if dfyi == True:
            s = []
            if updates:  # проверка, были ли обновления
                for element in updates:  # проход по всем обновлениям в ответе
                    s.append(element)
                data[0]['ts'] = response['ts']
                
                otvet1=[]
                for i in range(len(s)):
                    otvet = {}
                    types = s[i][0]
                    
                    if types == 4:
                        if s[i][2]==49:
                            otvet["type"] = "message_new"
                            otvet["params"] = {"peer_id":s[i][3],
                                               "text": s[i][5],
                                               "message_id":s[i][1],
                                               "time":unixtime_converter(s[i][4]),
                                               }
                        else:
                            otvet["type"] = "message_from_me"
                            otvet["params"] = {"peer_id":s[i][3],
                                               "text": s[i][5],
                                               "message_id":s[i][1],
                                               "time":unixtime_converter(s[i][4]),
                                               }
                    elif types == 8:
                        otvet["type"] = "friend_online"
                        otvet["params"] = {"peer_id":-s[i][1],
                                           "time":unixtime_converter(s[i][3]),
                                           "type":compucter_opredeli(s[i][2])}
                    elif types == 9:
                        otvet["type"] = "friend_offline"
                        if s[i][2] == 0:
                            xima ="offline by leave"
                        if s[i][2] == 1:
                            xima = "offline by timeout"
                        otvet["params"] = {"peer_id":-s[i][1],
                                           "time":unixtime_converter(s[i][3]),
                                           "offline_type":xima}
                        
                    elif types == 13:
                        otvet["type"] = "messages_all_deleted"
                    elif types == 14:
                        otvet["type"] = "message_restored"
                    elif types == 51:
                        otvet["type"] = "chat_edit"
                    elif types == 61:
                        otvet["type"] = "message_type"
                        otvet["params"]={"peer_id":s[i][1]}
                    elif types == 62:
                        otvet["type"] = "message_type_chat"
                    elif types == 80:
                        otvet["type"] = "messages_count"
                        otvet["params"] ={"count":s[i][1]}
                    elif types == 112 :
                        otvet["type"] = "notifications_change"
                    elif types == 3 or types ==2:
                        if len(s[i])>=3:
                            
                                if s[i][3] > 200000000:
                                    id_bot = s[i][3]
                                else:
                                    id_bot = -s[i][3]
                                otvet["type"] = message_flag(s[i][2])
                                otvet["params"] = {"message_id":s[i][1],
                                                   "peer_id":id_bot 
                                              }
                        else:
                            otvet["type"] = message_flag(s[i][2])
                            
                    elif types == 6 or types == 7:
                        otvet["type"] = "message_readed"
                    else:
                        otvet["type"]= "not_definded"
                    otvet1.append(otvet)
                    otvet = {}
                if 1 == 1:
                    if otvet1 != {}:
                        return otvet1
                    else:
                        return None             
            
        
    def longpoll_bot(szenarii1,szenarii2,message_neznayu="я не знаю, как ответить(((",attachment_neznayu="doc302808715_475715032",attachments = None,vk=None,login=None,password=None,token=None):
        """чат-бот с использованием longpoll api"""
        """
        szenarii1 - list в котором лежат сценарии(варианты того, что может прислать пользователь)
        szenarii2 - list, в котором лжат ответы на сценарии(на первый элемент
            szenarii1 будет отвечен первый элемент szenarii1, длина массива szenarii2 должна быть равна
                длине szenarii1
        message_neznayu - строка, в которой ответ на все другие сообщения, не считая 
        attachment_neznayu - attachment, который пошлется, если 




        """

        if len(szenarii1)!=len(szenarii2):
            raise OSError("длина szenarii2 должна быть равна длене szenarii1")
        if vk ==None:
            if token!=None:
                vk = bot_vk.auth_vk(token = token)
            elif login!=None and password!=None:
                vk = bot_vk.auth_vk(login = login,password = password)
                
            else:
                raise OSError("нужен или логин с паролем или токен или параметр vk")
        if attachments == None:
            attachments=[""]*len(szenarii1)
        
        id_own = vk.method("users.get",{})[0]["id"]
        
        while True:
            info =bot_vk.longpoll.user_longpoll(vk)
            
            if info != None:
                q = 0
                
                for i in info:
                    if i["type"] == "message_new":
                        
                        q = 1
                        info = i
                        break
                
                if q ==1:
                    id = info["params"]["peer_id"]
                    message = info["params"]["text"]
                    if id != id_own and id>0:
                        
                        ininon = vk.method("users.get",{"user_ids":id,"fields":"id,city,sex"})[0]
                        firstname = ininon["first_name"]
                        lastname =ininon["last_name"]
                        if "city" in ininon:
                            city = ininon["city"]["title"]
                        else:
                            city = "Москва"
                        pol = ininon["sex"]
                        

                        
                        s = 1
                        
                        for i in range(len(szenarii1)):
                            mes =szenarii1[i]
                            if mes.lower() == message.lower():
                                s = 0
                                
                                string = bot_vk.parse(szenarii2[i], pol).format(firstname=firstname,lastname=lastname,city=city)
                                                                     
                                vk.method("messages.send",{"message":string,"peer_id":id,"attachment": attachments[i]})
                                
                                break
                                        
                        if s == 1:
                            
                            string = bot_vk.parse(message_neznayu, pol).format(firstname=firstname,lastname=lastname,city=city)
                            
                            vk.method("messages.send",{"message":string,"peer_id":id,"attachment":attachment_neznayu})
                           
                 
