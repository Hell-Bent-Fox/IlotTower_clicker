from telethon import TelegramClient
import asyncio
api_id = 6368136
api_hash = 'ca47bb40113dab4948204cf06b1b3f86'
bot_name="IlotTower"
client = TelegramClient('session_name3', api_id, api_hash)
client.start()
# tegmo=False
# di = client.get_dialogs()
# for dialog in di:
#     print(dialog)
#     if dialog.title == bot_name:
#         tegmo = dialog
# print(tegmo)
# client.run_until_disconnected()