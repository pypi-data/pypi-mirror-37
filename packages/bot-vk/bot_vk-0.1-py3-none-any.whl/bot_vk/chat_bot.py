import random
import datetime
import time
def get_time():
    def strTimeProp(start, end, format, prop):
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))


    def randomDate(start, end, prop):
        return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)

    return randomDate(datetime.datetime.strftime(datetime.datetime.today(),'%m/%d/%Y %I:%M %p'), datetime.datetime.strftime(datetime.datetime.today()+datetime.timedelta(days=10000),'%m/%d/%Y %I:%M %p'), random.random())
    

class chat():
    def random_chat_person(vk,chat_id):
        info = vk.method("messages.getConversationMembers",{"peer_id":chat_id})
        
        count_id=[] 
        
        for i in info["profiles"]:
            
            
            count_id.append("И этот человек:\n@id{id}({last_name} {first_name})".format(id = str(i["id"]),last_name=i["last_name"],first_name=i["first_name"]))
            
        return random.choice(count_id)
    def random_date():
        return "И это случиться "+ get_time()
    def True_Flase():
        return random.choice(["и это правда!!!", "и это неправда!!!"])

