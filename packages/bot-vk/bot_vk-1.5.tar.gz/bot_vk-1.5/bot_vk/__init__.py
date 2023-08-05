from .keyboard_for_bot import keyboard
from .bot_python import internet_on,auth_vk,dele,vk_bot,parse
from .bot_longpoll import longpoll
from .chat_bot import chat
from .music import Music

music,bot_longpoll,bot_python,keyboard_for_bot,chat_bot = None,None,None,None,None
globals().pop("bot_longpoll"),globals().pop("chat_bot"),globals().pop("bot_python"),globals().pop("keyboard_for_bot"),globals().pop("music")


__version__ = "1.5"
__email__ = "imartemy1524@gmail.com"
__vk__ = "https://vk.com/imartemy"
__doc__="https://vk.com/@bot_vk_python-doc-1-0"
__url__="https://vk.com/@bot_vk_python-doc-1-0"
name="bot_vk"
