import random
import json
class keyboard():
    def get(text, side,color = None,one_time = True):
        """модуль позволяет создать свою клавиатуру"""
        """
        text - list, в котором каждый элемент соответствует своей кнопке. Пример:
                list = ["начать","назад"]
        color - list, в котором каждый элемент соответствует цвету кнопки.
            Если не передано, то генерируется случайное значение. 
        side - на каком уровне находится кнопка. На одном уровне больше 4-х кнопок недопустимо. Пример:
                side = [1,1,1,2,3]
        one_time - сразу ли исчезнит клавиатура. Если False - то нет.Если вы набрали False, а потом хотите. чтобы она исчезла, то в параметре клавиатуры
            передайте функцию keyboard_none(ниже)
        """
        
        count = len(text)
        if color == None:
            s = ["default","negative","primary","positive"]
            color = []
            for i in range(count):
                color.append(random.choice(s))
        for i in range(len(color)):
            if color[i].lower() == "green":
                color[i] = "positive"
            elif color[i].lower()== "blue":
                color[i] = "primary"
            elif color[i].lower() == "white":
                color[i] = "default"
            elif color[i].lower() ==  "red":
                color[i] = "negative"
        """
        if side == None:
            
            side = []
            for i in range(count):
                side.append(i+1)
        """        
        if len(color) == len(text):
            def get_button(label, color, payload=""):
                return {
                    "action": {
                        "type": "text",
                        'payload': json.dumps(payload),
                        "label": label
                    },
                    "color": color
                }
            def get(count):
                zi = []
                cou = 1
                s1 = []
                for i in range(count):
                    
                    if cou == side[i]:
                        
                        s1.append(get_button(label = text[i],color = color[i]))
                    else:
                        zi.append(s1)
                        s1 = []
                        cou +=1
                        s1.append(get_button(label = text[i],color = color[i]))
                zi.append(s1)
                return zi
            keyboard_hello = {
            "one_time": one_time,
            "buttons": get(count)
            }
            keyboard_hello  = json.dumps(keyboard_hello, ensure_ascii=False).encode('utf-8')
            keyboard_hello = str(keyboard_hello.decode('utf-8'))

            return keyboard_hello
    def keyboard_none():
        """модуль возращает пустую клавиатуру"""
        keyboard_None = {
            "one_time": True,
            "buttons": []
        }
        keyboard_None  = json.dumps(keyboard_None, ensure_ascii=False).encode('utf-8')
        keyboard_None = str(keyboard_None.decode('utf-8'))
        return keyboard_None             
            
