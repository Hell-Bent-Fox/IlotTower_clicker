# from telethon import TelegramClient, sync,events
# api_id = 4943278
# api_hash = 'd27d073b2207ce0cdf8b5012371dad78'
# bot_name="IlotTower"
# chat_name=bot_name
# client = TelegramClient('session_name2', api_id, api_hash)
# client.start()
# # tegmo=False
# # for dialog in client.get_dialogs():
# #     print(dialog)
# #     if dialog.title == bot_name:
# #         tegmo = dialog
# # print(tegmo)
# line=client.get_messages(chat_name, limit=1)
# for i in line:
#     print(i)
# button_text=line[0].reply_markup.rows[0].buttons[0].text
# print(button_text)
# line[0].click(text=button_text)
#
# client.run_until_disconnected()
import subprocess
import sys
import threading  # Потоки
def start_bot(name):
    p= subprocess.Popen([sys.executable, 'main.py'],stdin=subprocess.PIPE,shell=False,text=True)
    p.communicate(input=name)
    p.wait()
account=['session_name3','session_name2','session_name']
# account=['session_name3']
threads=[]
for i in account:
    t=threading.Thread(target=start_bot, daemon=True,name=i,args=(i,))
    t.start()
    threads.append(t)
[thread.join() for thread in threads]