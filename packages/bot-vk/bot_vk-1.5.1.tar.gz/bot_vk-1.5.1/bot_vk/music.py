import lxml.html
import requests
import re
from itertools import islice
from bs4 import BeautifulSoup
import bot_vk
import re
import vk_api
import bot_vk
ine = []
class Music(object):
    """парсинг музыки с вк"""
    def __init__(self,vk):
        self.vk = vk
        """параметр bot_vk.auth_vk с авторизацией ЛОГИНА И ПАРОЛЯ"""
    def auth_for_music(self):
        """создает куки для парсинга музыки"""
        login = self.vk.login
        password=self.vk.password

        url = 'http://vk.com/'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'DNT':'1'
        }
        session = requests.session()
        data = session.get(url, headers=headers)
        page = lxml.html.fromstring(data.content)

        form = page.forms[0]

        form.fields['email'] = login
        form.fields['pass'] = password

        #авторизовываемя для получения музыки
        response = session.post(form.action, data=form.form_values())
        ine.append(session)
    def get(self,user_id=None):
        """получает музыку пользователя"""
        if ine == []:
            self.auth_for_music()
        
        response = ine[0].post("https://vk.com/audios"+str(user_id))
            

        #da = re.findall('data-audio="\[(.+)\]',response.text)
        da = re.findall('data-full-id="(.+?)"',response.text)
        for i in range(len(da)):
            da[i] = "audio"+da[i]
        if da != []:
            
            return da
        else:
            raise NameError ("У пользователя нет музыки, или он ограничел к ней доступ")
    def get_url(self,attachment):
        sen = []
        sen1=[]
        while attachment != []:
            qiy = ""
            for i in range(len(attachment)):
                if i <10:                    
                    qiy+=attachment[i]+","
                else:
                    break
            for i in range(len(attachment)):
                if i<10:
                    attachment.pop(0)
                else:
                    break 
            qiy.split(",")        
                      
            s = self.vk.method("messages.send",{"user_id":472427950,"attachment":"audio"+str(qiy)})
            q = self.vk.method("messages.getById",{"message_ids":s})["items"][0]["attachments"]
            self.vk.method("messages.delete",{"message_ids":s})
            for i in q:
                sen.append(i["audio"]["url"])
                sen1.append(i["audio"]["artist"]+" || "+i["audio"]["title"])
        return sen,sen1
