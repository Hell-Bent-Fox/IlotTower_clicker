from telethon import TelegramClient, sync,events
import asyncio
import time
import ast
from telethon import errors
import os.path
# Вставляем api_id и api_hash
# api_id = 5342376
# api_hash = '5ffe37fa57d82708537abff7c69b94e0'
# bot_name="IlotTower"
# chat_name=bot_name
# client = TelegramClient('session_name', api_id, api_hash)
api_id = 4943278
api_hash = 'd27d073b2207ce0cdf8b5012371dad78'
bot_name="IlotTower"
chat_name=bot_name
session=str(input())
# client = TelegramClient('session_name2', api_id, api_hash)
client = TelegramClient(session, api_id, api_hash)
client.flood_sleep_threshold=200
# target_info={'1':{"heal_shop":'0;-1'}}
#---------------------
# player_info={"main_task":'task',"second_task":'task',"third_task":'task',"player_level":'1',"health":'190',"max_health":'190',"position":'0;0;1',"heal_comand":''}
# main_task: buy_heal,farm_exp,sell_res
# second_task: walk_to_point(0;0)
# third_task: fight, heal, buy_heal, sell_res
def take_player_info_fun():
    if not(os.path.isfile('player_{0}.txt'.format(session))):
        put_player_info_fun({"main_task":'farm_exp',"second_task":'walk_to_point(0;0;1)',"third_task":'fight',"player_level":'1',"health":'190',"max_health":'190',"position":'0;0;1',"heal_comand":''})
    player_file = open('player_{0}.txt'.format(session), 'r')
    player_info = ast.literal_eval(player_file.read())
    player_file.close()
    return player_info
def put_player_info_fun(p_inf):
    player_file = open('player_{0}.txt'.format(session), 'w')
    player_file.write(str(p_inf))
    player_file.close()
def take_target_info_fun():
    target_file = open('target.txt', 'r')
    target_info = ast.literal_eval(target_file.read())
    target_file.close()
    return target_info
def put_target_info_fun(t_inf):
    target_file = open('target.txt', 'w')
    target_file.write(str(t_inf))
    target_file.close()
async def fight(chat_name,def_event,hight_level):
    # message_from_bot = client.get_messages(chat_name, limit=1)
    # print(message_from_bot.stringify())
    # print(message_from_bot.reply_markup.rows[0].buttons[0].text)
    message_from_bot=def_event.message
    text = (message_from_bot.message)
    if text=='Чудовища поблизости не найдены' or 'не расправился с монстром' in text or 'не расправилась с монстром' in text or 'Не отвлекайся' in text or 'не найдешь' in text or 'никого не нашел' in text or 'Не время смотреть в рюкзак' in text or 'никого не нашла' in text:
        if 'не расправился с монстром' in text or 'не расправилась с монстром' in text or 'Не отвлекайся' in text:
            print("Убей монстра вручную")
        else:
            await asyncio.gather(asyncio.create_task(move(chat_name, def_event)))
    else:
        if text.startswith('Нападение'):
            time.sleep(7)
        elif text=='Тебе удалось сбежать.':
            try:
                await client.send_message(chat_name,'/monsters')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '/monsters')
                time.sleep(1)
        elif message_from_bot.reply_markup!=None and str(message_from_bot.reply_markup).startswith('ReplyInlineMarkup'):
            k=[i-1 for i in range(len(text.split(' '))) if 'уров' in text.split(' ')[i] and text.split(' ')[i-1].isdigit() and i>0]
            if text.split()[k[0]].isdigit():
                mob_level=text.split()[k[0]]
                print("HEREAGAIN lev=",mob_level)
                # print(message_from_bot.reply_markup.rows[0].buttons[0].text)
                if int(mob_level)==1 or int(mob_level)<int(hight_level)-1:
                    button_text=message_from_bot.reply_markup.rows[0].buttons[0].text
                    try:
                        await message_from_bot.click(text=button_text)
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await message_from_bot.click(text=button_text)
                        time.sleep(1)
                else:
                    button_text=message_from_bot.reply_markup.rows[0].buttons[1].text
                    try:
                        await message_from_bot.click(text=button_text)
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await message_from_bot.click(text=button_text)
                        time.sleep(1)
        elif 'одержал победу' in text or 'одержала победу' in text:
            if text.split()[1][2:-1].isdigit():
                player_info = take_player_info_fun()
                if int(text.split()[1][2:-1])<int(player_info['max_health'])//2+int(player_info['max_health'])//5:
                    player_info['health'] = text.split()[1][2:-1]
                    player_info['third_task'] = 'heal'
                    put_player_info_fun(player_info)
                    try:
                        await client.send_message(chat_name, '🎒 Рюкзак')
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await client.send_message(chat_name, '🎒 Рюкзак')
                        time.sleep(1)
                else:
                    try:
                        await client.send_message(chat_name, '/monsters')
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await client.send_message(chat_name, '/monsters')
                        time.sleep(1)
        elif 'Ты погибаешь' in text or 'пал в бою' in text or 'пала в бою' in text or 'раненое тело принесли' in text:
            pass
        else:
            try:
                await client.send_message(chat_name, '/monsters')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '/monsters')
                time.sleep(1)
async def heal(chat_name,def_event):
    player_info = take_player_info_fun()
    message_from_bot = def_event.message
    text = (message_from_bot.message)
    helth=player_info['health']
    max_health=player_info['max_health']
    print(text)
    if 'нет этого зелья' in text:
        player_info['heal_comand'] = ''
        put_player_info_fun(player_info)
        try:
            await client.send_message(chat_name, '🎒 Рюкзак')
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name, '🎒 Рюкзак')
            time.sleep(1)
    if 'здоровье восстановлено до максимума' in text or 'здоров, как бык' in text:
        player_info['heal_comand'] = ''
        player_info['third_task'] = 'fight'
        put_player_info_fun(player_info)
        try:
            await client.send_message(chat_name, '🔍 Осмотреться')
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name, '🔍 Осмотреться')
            time.sleep(1)
    elif "здоровье восстановлено" in text:
        if(int(text.split(' ')[-1])*2+int(helth)<=int(max_health)):
            player_info['health'] = str(int(player_info['health'])+int(text.split(' ')[-1]))
            put_player_info_fun(player_info)
            try:
                await client.send_message(chat_name, player_info['heal_comand'])
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, player_info['heal_comand'])
                time.sleep(1)
        else:
            player_info['heal_comand']=''
            player_info['third_task']='fight'
            put_player_info_fun(player_info)
            try:
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
    elif text.startswith('Алхимия'):
        try:
            await client.send_message(chat_name, player_info['heal_comand'])
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name, player_info['heal_comand'])
            time.sleep(1)
async def buy_heal(chat_name,def_event):
    if'лавка' in def_event.message.message.lower().split('\n')[0]:
        best_choice=min([int(j[2][1:])/int(j[0][1:]) for j in [i.split(' ')[-4:-1] for i in def_event.message.message.split('\n')[2:]]])
        best_index=([int(j[2][1:])/int(j[0][1:]) for j in [i.split(' ')[-4:-1] for i in def_event.message.message.split('\n')[2:]]].index(best_choice))
        try:
            await client.send_message(chat_name,[i.split(' ')[-1] for i in def_event.message.message.split('\n')[2:]][best_index])
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name,[i.split(' ')[-1] for i in def_event.message.message.split('\n')[2:]][best_index])
            time.sleep(1)
    elif 'был куплен' in def_event.message.message.split('\n')[0]:
        line=await asyncio.gather(asyncio.create_task(client.get_messages(chat_name, limit=2)))
        kol=int(line[0][0].message.split('\n')[1].split(' ')[-1][1:])//int(line[0][0].message.split('\n')[0].split(' ')[-1][1:-1])
        player_info = take_player_info_fun()
        player_info['heal_comand'] = ''
        player_info['main_task'] = 'farm_exp'
        put_player_info_fun(player_info)
        if kol>0:
            if kol<=200:
                try:
                    await client.send_message(chat_name,line[0][1].message.split('_')[0]+'_'+line[0][1].message.split('_')[1]+'_'+str(kol))
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name,line[0][1].message.split('_')[0] + '_' + line[0][1].message.split('_')[1] + '_' + str(kol))
                    time.sleep(1)
            else:
                try:
                    await client.send_message(chat_name,line[0][1].message.split('_')[0] + '_' + line[0][1].message.split('_')[1] + '_' + str(200))
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name,line[0][1].message.split('_')[0] + '_' + line[0][1].message.split('_')[1] + '_' + str(200))
                    time.sleep(1)
        else:
            try:
                await client.send_message(chat_name,'💡 Герой')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '💡 Герой')
                time.sleep(1)
        time.sleep(1)
def distance(x1,y1,x2,y2):
    import math
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
async def move(chat_name,def_event):
    player_info = take_player_info_fun()
    target_info = take_target_info_fun()
    if str(player_info['position'].split(';')[2]) not in target_info.keys():
        target_info[str(player_info['position'].split(';')[2])] = {"heal_shop": None, "sell_shop": None, "север": None,"восток": None, "юг": None, "запад": None}
    import random
    if player_info['second_task'].split('(')[1][:-1]==player_info['position']:
        a = [(target_info[str(player_info['position'].split(';')[2])]['восток']),
                    (target_info[str(player_info['position'].split(';')[2])]['запад'])]
        b = [(target_info[str(player_info['position'].split(';')[2])]['север']),
                    (target_info[str(player_info['position'].split(';')[2])]['юг'])]
        for i in range(2):
            if a[i]!=None:
                a[i]=int(a[i])
            else:
                a[i]=10000000
                if i==0:
                    a[i]=a[i]*(-1)
            if b[i]!=None:
                b[i]=int(a[i])
            else:
                b[i]=10000000
                if i==0:
                    b[i]=b[i]*(-1)
        a=sorted(a)
        b=sorted(b)
        player_info['second_task']=(player_info['second_task'].split('(')[0] +'('+ str(random.randint(a[0], a[1])) + ';'+str(random.randint(b[0], b[1])) + ';' +str(player_info['position'].split(';')[2])+')')
        put_player_info_fun(player_info)
    target_x=int(player_info['second_task'].split('(')[1][:-1].split(';')[0])
    target_y=int(player_info['second_task'].split('(')[1][:-1].split(';')[1])
    now_x=int(player_info['position'].split(';')[0])
    now_y=int(player_info['position'].split(';')[1])
    road=[distance(now_x,now_y+1,target_x,target_y),distance(now_x+1,now_y,target_x,target_y),distance(now_x,now_y-1,target_x,target_y),distance(now_x-1,now_y,target_x,target_y)]
    next_move=[]
    for i in road:
        if i==min(road):
            next_move.append(i)
        else:
            next_move.append(None)
    print(next_move)
    i=random.randint(0,3)
    while next_move[i]==None:
        i=random.randint(0,3)
    option=['⬆️ Север','➡️ Восток','⬇️ Юг','⬅️ Запад']
    player_info["last_move"]=option[i].split(' ')[-1].lower()
    put_player_info_fun(player_info)
    try:
        await client.send_message(chat_name, option[i])
        time.sleep(1)
    except errors.FloodWaitError as e:
        print('Flood waited for', e)
        await client.send_message(chat_name, option[i])
        time.sleep(1)
async def sell(chat_name,def_event):
    message_from_bot = def_event.message
    text = (message_from_bot.message)
    i=0
    count_mass=[]
    comand_mass=[]
    while i <len(text.split('\n')):
        count_mass.append(text.split('\n')[i].split('-')[0].split('(')[-1].split(')')[0])
        comand_mass.append(text.split('\n')[i].split('-')[1].split(' ')[-1])
        i+=1
    print(count_mass)
    print(comand_mass)
    for i in range(len(count_mass)):
        try:
            await client.send_message(chat_name, comand_mass[i].split('_')[0]+'_'+comand_mass[i].split('_')[1]+'_'+count_mass[i])
            time.sleep(3)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name,comand_mass[i].split('_')[0] + '_' + comand_mass[i].split('_')[1] + '_' +count_mass[i])
            time.sleep(3)
    try:
        await client.send_message(chat_name, '🔍 Осмотреться')
        time.sleep(1)
    except errors.FloodWaitError as e:
        print('Flood waited for', e)
        await client.send_message(chat_name, '🔍 Осмотреться')
        time.sleep(1)
@client.on(events.MessageEdited(chats=(chat_name)))
@client.on(events.NewMessage(chats=(chat_name)))
async def normal_handler(event):
    time.sleep(0.3)
    print(event.message)
    player_info = take_player_info_fun()
    target_info = take_target_info_fun()
    print(player_info)
    # if 'Прогресс выполнения'in event.message.message:
    #     pass
    if 'Край карты' in event.message.message:
        if player_info['last_move'] in ['север','юг']:
            new_cord=str(player_info['position'].split(';')[1])
        elif player_info['last_move'] in ['восток','запад']:
            new_cord=str(player_info['position'].split(';')[0])
        else:
            new_cord=None
        target_info[str(player_info['position'].split(';')[2])][player_info['last_move']]=new_cord
        put_target_info_fun(target_info)
        player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' + str(player_info['position'])+')')
        put_player_info_fun(player_info)
        try:
            await client.send_message(chat_name, '🔍 Осмотреться')
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name, '🔍 Осмотреться')
            time.sleep(1)
    elif 'не смог пойти дальше' in event.message.message or 'не смогла пойти дальше' in event.message.message:
        time.sleep(3)
        try:
            await asyncio.gather(asyncio.create_task(move(chat_name, event)))
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await asyncio.gather(asyncio.create_task(move(chat_name, event)))
            time.sleep(1)
    elif 'Ты погибаешь' in event.message.message or 'Ты еще в дороге' in event.message.message or 'пал в бою' in event.message.message or 'пала в бою' in event.message.message or 'раненое тело принесли' in event.message.message:
        pass
    elif len([i for i in ['север', 'восток', 'юг','запад','южного'] if i in event.message.message.lower()])>0 or 'был продан' in event.message.message:
        pass
    elif 'Тебя подлатали' in event.message.message:
        try:
            await client.send_message(chat_name, '💡 Герой')
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name, '💡 Герой')
            time.sleep(1)
    elif 'недостаточно 💰 для покупки' in event.message.message:
        player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' +target_info[str(player_info['position'].split(';')[2])]['sell_shop'] + ';' + str(player_info['position'].split(';')[2]) + ')')
        player_info['main_task'] = 'sell_res'
        put_player_info_fun(player_info)
        try:
            await client.send_message(chat_name, '🔍 Осмотреться')
            time.sleep(1)
        except errors.FloodWaitError as e:
            print('Flood waited for', e)
            await client.send_message(chat_name, '🔍 Осмотреться')
            time.sleep(1)
    elif event.message.message.split('\n')[0].startswith('👨') or event.message.message.split('\n')[0].startswith('👩'):
        # person_level = client.get_messages(chat_name, limit=1)[0].message.split('\n')[1].split(' ')[1]
        person_level = event.message.message.split('\n')[1].split(' ')[1]
        player_info['max_health'] = event.message.message.split('\n')[2].split(' ')[2].split('/')[1]
        if (float(event.message.message.split()[event.message.message.split().index('🎒Рюкзак') + 1].split('/')[0].replace(',', '.')) + 30 > float(event.message.message.split()[event.message.message.split().index('🎒Рюкзак') + 1].split('/')[1].replace(',', '.')) and person_level != '1') or (float(event.message.message.split()[event.message.message.split().index('🎒Рюкзак') + 1].split('/')[0].replace(',', '.')) + 5 > float(event.message.message.split()[event.message.message.split().index('🎒Рюкзак') + 1].split('/')[1].replace(',', '.'))):
            player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' +target_info[str(player_info['position'].split(';')[2])]['sell_shop'] + ';' + str(player_info['position'].split(';')[2]) + ')')
            player_info['main_task'] = 'sell_res'
            put_player_info_fun(player_info)
            try:
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
        elif int(event.message.message.split('\n')[2].split(' ')[2].split('/')[0])<int(player_info['max_health'])//2+int(player_info['max_health'])//5:
            player_info['health']=event.message.message.split('\n')[2].split(' ')[2].split('/')[0]
            player_info['third_task']='heal'
            try:
                await client.send_message(chat_name, '🎒 Рюкзак')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '🎒 Рюкзак')
                time.sleep(1)
            time.sleep(1)
        else:
            player_info['main_task']='farm_exp'
            player_info['third_task']='fight'
            try:
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
        player_info['player_level']=person_level
        put_player_info_fun(player_info)
    elif None in target_info[str(player_info['position'].split(';')[2])].values():
        if 'здесь:' in event.message.message.split('\n')[0]:
            cord = (event.message.message.split('\n')[0].split(' ')[-1][1:-1].split(':'))
            # floor = (event.message.message.split('\n')[0].split(' ')[-3])
            floor = (event.message.message.split('\n')[0].split('Этаж')[0].strip().split(' ')[-1])
            player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
            if str(floor) != player_info['second_task'].split('(')[1][:-1].split(';')[2].split(')')[0]:
                player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' + str(player_info['position']) + ')')
            put_player_info_fun(player_info)
            if 'Постройки' in event.message.message and 'лавка' in event.message.message.lower() and target_info[str(player_info['position'].split(';')[2])]["heal_shop"]==None:
                target_info[str(player_info['position'].split(';')[2])]["heal_shop"]=str(cord[0][2:]) + ';' + str(cord[1][2:])
                put_target_info_fun(target_info)
            if 'NPC поблизости' in event.message.message and '/npc' in event.message.message and target_info[str(player_info['position'].split(';')[2])]["sell_shop"]==None:
                try:
                    await client.send_message(chat_name, '/npc')
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, '/npc')
                    time.sleep(1)
            else:
                try:
                    await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                    time.sleep(1)
        elif 'поговорить' in event.message.message.split('\n')[0]and target_info[str(player_info['position'].split(';')[2])]["sell_shop"]==None:
            if 'Начать торговлю' in event.message.message:
                target_info[str(player_info['position'].split(';')[2])]["sell_shop"]=str(player_info['position']).split(';')[0]+';'+str(player_info['position']).split(';')[1]
                put_target_info_fun(target_info)
            try:
                await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                time.sleep(1)
            # target_info={'1':{"heal_shop":'0;-1',"sell_shop":'0;-9',"север":'7',"восток":'7',"юг":'-12',"запад":'-12'},'2':{"heal_shop":'1;1',"sell_shop":'5;-6',"север":'8',"восток":'7',"юг":'-7',"запад":'-8'}}
        if 'до точки' in event.message.message.split('\n')[0]:
            cord = (event.message.message.split('\n')[1].split(' ')[-1][1:-1].split(':'))
            # floor = (event.message.message.split('\n')[1].split(' ')[1])
            floor = (event.message.message.split('\n')[1].split('Этаж')[0].strip().split(' ')[-1])
            player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
            put_player_info_fun(player_info)
            try:
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
    elif 'новый уровень' in event.message.message:
        player_info['player_level']=str(int(player_info['player_level'])+1)
        player_info['third_task'] = 'fight'
        put_player_info_fun(player_info)
    elif player_info['main_task']=='farm_exp':
        if player_info['third_task'] == 'fight':
            if 'здесь:' in event.message.message.split('\n')[0]:
                cord=(event.message.message.split('\n')[0].split(' ')[-1][1:-1].split(':'))
                # floor=(event.message.message.split('\n')[0].split(' ')[-3])
                floor = (event.message.message.split('\n')[0].split('Этаж')[0].strip().split(' ')[-1])
                player_info['position']=str(cord[0][2:])+';'+str(cord[1][2:])+';'+str(floor)
                if str(floor)!=player_info['second_task'].split('(')[1][:-1].split(';')[2].split(')')[0]:
                    player_info['second_task'] =(player_info['second_task'].split('(')[0] + '(' + str(player_info['position'])+')')
                put_player_info_fun(player_info)
            if 'до точки' in event.message.message.split('\n')[0]:
                cord=(event.message.message.split('\n')[1].split(' ')[-1][1:-1].split(':'))
                # floor=(event.message.message.split('\n')[1].split(' ')[1])
                floor = (event.message.message.split('\n')[1].split('Этаж')[0].strip().split(' ')[-1])
                player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
                put_player_info_fun(player_info)
                try:
                    await client.send_message(chat_name, '🔍 Осмотреться')
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, '🔍 Осмотреться')
                    time.sleep(1)
            else:
                person_level=player_info['player_level']
                if '🌆' in event.message.message or 'Обрыв' in event.message.message:
                    await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                else:
                    await asyncio.gather(asyncio.create_task(fight(chat_name, event,person_level)))
        elif player_info['third_task'] == 'heal':
            if 'был куплен' in event.message.message.split('\n')[0]:
                try:
                    await client.send_message(chat_name, '💡 Герой')
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, '💡 Герой')
                    time.sleep(1)
                #Проверить
            elif 'Не хватает места' in event.message.message:
                player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' +target_info[str(player_info['position'].split(';')[2])]['sell_shop'] + ';' + str(player_info['position'].split(';')[2]) + ')')
                player_info['main_task'] = 'sell_res'
                put_player_info_fun(player_info)
                try:
                    await client.send_message(chat_name, '🔍 Осмотреться')
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, '🔍 Осмотреться')
                    time.sleep(1)
            elif event.message.message.startswith('Экипировано'):
                comand_to_heal=[j for j in [i.split(' ') for i in event.message.message.split('\n')] if j[0]=='Алхимия:']
                print("HERE",comand_to_heal)
                try:
                    await client.send_message(chat_name, comand_to_heal[0][1])
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, comand_to_heal[0][1])
                    time.sleep(1)
            elif event.message.message.startswith('Алхимия'):
                if len(event.message.message.split('\n'))>1 and (event.message.message.split('\n')[1]!='Пусто'):
                    if player_info['heal_comand'] == '':
                        player_info['heal_comand'] = event.message.message.split('\n')[1].split(' ')[-1]
                        put_player_info_fun(player_info)
                        print("HERE", player_info)
                else:
                    player_info['second_task']=(player_info['second_task'].split('(')[0] + '(' + target_info[str(player_info['position'].split(';')[2])]['heal_shop']  +';'+str(player_info['position'].split(';')[2])+')')
                    player_info['heal_comand'] =''
                    player_info['main_task'] = 'buy_heal'
                    put_player_info_fun(player_info)
                    try:
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
            if player_info['heal_comand']!='':
                await asyncio.gather(asyncio.create_task(heal(chat_name, event)))
    elif player_info['main_task']=='buy_heal':
        if 'до точки' in event.message.message.split('\n')[0]:
            cord = (event.message.message.split('\n')[1].split(' ')[-1][1:-1].split(':'))
            # floor = (event.message.message.split('\n')[1].split(' ')[1])
            floor = (event.message.message.split('\n')[1].split('Этаж')[0].strip().split(' ')[-1])
            player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
            put_player_info_fun(player_info)
            if target_info[str(player_info['position'].split(';')[2])]['heal_shop']==None:
                print("Нет координат магазина-аптеки")
            else:
                if(str(player_info['position'].split(';')[0])+';'+str(player_info['position'].split(';')[1])!=target_info[str(player_info['position'].split(';')[2])]['heal_shop']):
                    await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                    #идем дальше
                elif (str(player_info['position'].split(';')[0])+';'+str(player_info['position'].split(';')[1])==target_info[str(player_info['position'].split(';')[2])]['heal_shop']):
                    try:
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
        elif 'здесь:' in event.message.message.split('\n')[0]:
            cord = (event.message.message.split('\n')[0].split(' ')[-1][1:-1].split(':'))
            # floor = (event.message.message.split('\n')[0].split(' ')[-3])
            floor = (event.message.message.split('\n')[0].split('Этаж')[0].strip().split(' ')[-1])
            player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
            if str(floor) != player_info['second_task'].split('(')[1][:-1].split(';')[2].split(')')[0]:
                player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' + str(player_info['position']) + ')')
            put_player_info_fun(player_info)
            if 'лавка' in event.message.message.lower():
                if 'лавка' in event.message.message:
                    comand=event.message.message.split('лавка')[1].split('\n')[0]
                elif 'Лавка' in event.message.message:
                    comand=event.message.message.split('Лавка')[1].split('\n')[0]
                print(comand)
                try:
                    await client.send_message(chat_name, comand)
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, comand)
                    time.sleep(1)
            else:
                await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                # идем дальше
        elif 'лавка' in event.message.message.lower().split('\n')[0]:
            if 'Что интересует?' in event.message.message.split('\n')[2]:
                button_text=event.message.reply_markup.rows[0].buttons[0].text
                try:
                    await event.message.click(text=button_text)
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await event.message.click(text=button_text)
                    time.sleep(1)
            elif 'Хочешь чего-то купить?' in event.message.message.split('\n')[2]:
                button_text=event.message.reply_markup.rows[0].buttons[0].text
                try:
                    await event.message.click(text=button_text)
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await event.message.click(text=button_text)
                    time.sleep(1)
            elif 'Великий воитель значит?' in event.message.message.split('\n')[2] or 'Великая воительница значит?' in event.message.message.split('\n')[2]:
                button_text=event.message.reply_markup.rows[0].buttons[2].text
                try:
                    await event.message.click(text=button_text)
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await event.message.click(text=button_text)
                    time.sleep(1)
            else:
                await asyncio.gather(asyncio.create_task(buy_heal(chat_name, event)))
        elif 'был куплен' in event.message.message.split('\n')[0]:
            await asyncio.gather(asyncio.create_task(buy_heal(chat_name, event)))
        elif 'Не хватает места' in event.message.message:
            player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' +target_info[str(player_info['position'].split(';')[2])]['sell_shop'] + ';' +str(player_info['position'].split(';')[2])+')')
            player_info['main_task'] = 'sell_res'
            put_player_info_fun(player_info)
            try:
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '🔍 Осмотреться')
                time.sleep(1)
        elif player_info['third_task'] == 'heal':
            if event.message.message.startswith('Экипировано'):
                comand_to_heal=[j for j in [i.split(' ') for i in event.message.message.split('\n')] if j[0]=='Алхимия:']
                try:
                    await client.send_message(chat_name, comand_to_heal[0][1])
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, comand_to_heal[0][1])
                    time.sleep(1)
            elif event.message.message.startswith('Алхимия'):
                if len(event.message.message.split('\n'))>1 and (event.message.message.split('\n')[1]!='Пусто'):
                    if player_info['heal_comand'] == '':
                        player_info['heal_comand'] = event.message.message.split('\n')[1].split(' ')[-1]
                        put_player_info_fun(player_info)
                else:
                    # player_info['second_task']=(player_info['second_task'].split('(')[0] + '(' +target_info[str(player_info['position'].split(';')[2])]['heal_shop'] +';'+player_info['second_task'].split('(')[1].split(';')[-1])
                    player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' +target_info[str(player_info['position'].split(';')[2])]['heal_shop'] + ';' +str(player_info['position'].split(';')[2])+')')
                    print(player_info['second_task'])
                    player_info['heal_comand'] =''
                    player_info['main_task'] = 'buy_heal'
                    put_player_info_fun(player_info)
                    try:
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
            if player_info['heal_comand']!='':
                await asyncio.gather(asyncio.create_task(heal(chat_name, event)))
    elif player_info['main_task'] == 'sell_res':
        if 'до точки' in event.message.message.split('\n')[0]:
            cord = (event.message.message.split('\n')[1].split(' ')[-1][1:-1].split(':'))
            # floor = (event.message.message.split('\n')[1].split(' ')[1])
            floor = (event.message.message.split('\n')[1].split('Этаж')[0].strip().split(' ')[-1])
            player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
            put_player_info_fun(player_info)
            if target_info[str(player_info['position'].split(';')[2])]['sell_shop']==None:
                print("Нет координат скупщика")
            else:
                if (str(player_info['position'].split(';')[0]) + ';' + str(player_info['position'].split(';')[1]) !=target_info[str(player_info['position'].split(';')[2])]['sell_shop']):
                    await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                    # идем дальше
                elif (str(player_info['position'].split(';')[0]) + ';' + str(player_info['position'].split(';')[1]) ==target_info[str(player_info['position'].split(';')[2])]['sell_shop']):
                    try:
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
                    except errors.FloodWaitError as e:
                        print('Flood waited for', e)
                        await client.send_message(chat_name, '🔍 Осмотреться')
                        time.sleep(1)
        elif 'здесь:' in event.message.message.split('\n')[0]:
            cord = (event.message.message.split('\n')[0].split(' ')[-1][1:-1].split(':'))
            # floor = (event.message.message.split('\n')[0].split(' ')[-3])
            floor = (event.message.message.split('\n')[0].split('Этаж')[0].strip().split(' ')[-1])
            player_info['position'] = str(cord[0][2:]) + ';' + str(cord[1][2:]) + ';' + str(floor)
            if str(floor) != player_info['second_task'].split('(')[1][:-1].split(';')[2].split(')')[0]:
                player_info['second_task'] = (player_info['second_task'].split('(')[0] + '(' + str(player_info['position']) + ')')
            put_player_info_fun(player_info)
            if '/npc' in event.message.message and (str(player_info['position'].split(';')[0]) + ';' + str(player_info['position'].split(';')[1]) ==target_info[str(player_info['position'].split(';')[2])]['sell_shop']):
                try:
                    await client.send_message(chat_name, '/npc')
                    time.sleep(1)
                except errors.FloodWaitError as e:
                    print('Flood waited for', e)
                    await client.send_message(chat_name, '/npc')
                    time.sleep(1)
            else:
                await asyncio.gather(asyncio.create_task(move(chat_name, event)))
                # идем дальше
        elif 'поговорить' in event.message.message.split('\n')[0]:
            try:
                await client.send_message(chat_name, event.message.message.split('\n')[2].split(' ')[-1])
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, event.message.message.split('\n')[2].split(' ')[-1])
                time.sleep(1)
        elif 'купить могу' in event.message.message.split('\n')[0]:
            button_text = event.message.reply_markup.rows[0].buttons[1].text
            try:
                await event.message.click(text=button_text)
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await event.message.click(text=button_text)
                time.sleep(1)
        elif '💰' in event.message.message:
            await asyncio.gather(asyncio.create_task(sell(chat_name, event)))
        if 'нечего покупать' in event.message.message.split('\n')[0]:
            player_info['main_task'] = 'farm_exp'
            put_player_info_fun(player_info)
            try:
                await client.send_message(chat_name, '💡 Герой')
                time.sleep(1)
            except errors.FloodWaitError as e:
                print('Flood waited for', e)
                await client.send_message(chat_name, '💡 Герой')
                time.sleep(1)
# player_info={"main_task":'farm_exp',"second_task":'walk_to_point(0;0;2)',"third_task":'fight',"player_level":'1',"health":'190',"max_health":'190',"position":'0;0;1',"last_move":'',"heal_comand":''}
# player_file = open('player.txt', 'w')
# player_file.write(str(player_info))
# player_file.close()
# target_info={'1':{"heal_shop":'0;-1',"sell_shop":'0;-9',"север":'7',"восток":'7',"юг":'-12',"запад":'-12'},'2':{"heal_shop":'1;1',"sell_shop":'5;-6',"север":'8',"восток":'7',"юг":'-7',"запад":'-8'}}
# target_file = open('target.txt', 'w')
# target_file.write(str(target_info))
# target_file.close()
client.start()
tegmo=False
for dialog in client.get_dialogs():
    # print(dialog)
    if dialog.title == bot_name:
        tegmo = dialog
# print(tegmo)

# line=client.get_messages(chat_name, limit=2)
# for i in line:
#     print(i.message)
target_info=take_target_info_fun()
player_info=take_player_info_fun()
player_info['main_task'] = 'farm_exp'
player_info['third_task'] = 'fight'
# del target_info['точки:']
# put_target_info_fun(target_info)
# target_info=take_target_info_fun()
# player_info['position']='0;0;3'
if str(player_info['position'].split(';')[2]) not in target_info.keys():
    target_info[str(player_info['position'].split(';')[2])] = {"heal_shop": None, "sell_shop": None, "север": None,"восток": None, "юг": None, "запад": None}
    put_target_info_fun(target_info)
    target_info = take_target_info_fun()
put_player_info_fun(player_info)
client.send_message(chat_name,'💡 Герой')
time.sleep(4)
# person_level=client.get_messages(chat_name, limit=1)[0].message.split('\n')[1].split(' ')[1]
# print(person_level)


# player_info={"main_task":'farm_exp',"second_task":'walk_to_point(0;0;1)',"third_task":'fight',"change_floor":{"old_flor":None,"new_floor":None},"player_level":'1',"health":'190',"max_health":'190',"position":'0;0;1',"heal_comand":''}
# locate_shop=[]
# for i in target_info.keys():
#     if(i<=player_info["position"].split(';')[-1]):
#         locate_shop.append(target_info[i]["heal_shop"])
# print(locate_shop)
# i=0
# while locate_shop[i]!=None and i<len(locate_shop):
#     i+=1
# print(locate_shop[i-1]+';'+list(target_info.keys())[i-1])
# if tegmo!=False:
#     fight(bot_name)

client.run_until_disconnected()

    # print(client.get_messages(bot_name, limit=1)[0].reply_markup.rows[0].buttons[1].text)
# resp = client(GetBotCallbackAnswerRequest(bot_name,message_id,data=button_data))
