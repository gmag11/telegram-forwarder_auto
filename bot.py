#    Copyright (c) 2021 Ayush
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License > .

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Basics
TO_ = config("TO_CHANNEL")
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
SHOW_SENDER = config("SHOW_SENDER", default=False, cast=bool)

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    tgClient = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    tgClient.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)


@tgClient.on(events.NewMessage(chats=FROM))
async def sender_bH(event):
    for i in TO:
        try:
            Message = event.message
            if SHOW_SENDER:
                sender = await event.get_sender()
                if sender.username is not None:
                    Username = "@" + sender.username
                else:
                    Username = sender.first_name
                    if sender.last_name is not None:
                        Username += f" {sender.last_name}"
                Message.message = Username + '\n' + event.message.message

            await tgClient.send_message(
                i,
                Message
            )
        except Exception as e:
            print(e)

print("Bot has started.")
tgClient.run_until_disconnected()
