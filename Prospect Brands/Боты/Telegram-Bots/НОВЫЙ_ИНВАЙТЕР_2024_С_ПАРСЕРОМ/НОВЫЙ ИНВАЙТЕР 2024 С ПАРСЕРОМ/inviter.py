from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.sync import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep
import random

#############################################
# --- НЕОБХОДИМО ЗАПОЛНИТЬ!!! ---
#
api_id = 1111111
api_hash = '11111111111111111111111111111'
# -Название чата или канала, куда приглашать юзеров (без @)
chat_name = 'Ваш айди чата - без собачки'

# Не трогать
# -Название файла, в котором хранятся userId (должен находится в одной директории со скриптом)
users_file = 'user_ids.txt'
device_model = "Pixel 3 XL"
system_version = "Android 10.0"

##########################################

if api_id == 0 or api_hash == 0:
    print(
        "Пожалуйста, перед запуском скрипта отредактируйте необходимые данные в нём! Вы не заполнили такие важные поля, как 'api_id' или 'api_hash'"
    )
    exit()

with TelegramClient('main_session', api_id, api_hash, device_model=device_model,
                    system_version=system_version) as client:
    try:
        with open(users_file, 'r') as file:
            user_ids = file.readlines()

        user_ids = [user_id.strip() for user_id in user_ids if user_id.strip()]

        # Присоединяемся к целевому чату перед инвайтом
        chat = client.get_entity(chat_name)
        client(JoinChannelRequest(chat))
        chat_id = chat.id


        for user_id in user_ids:
            try:
                print(user_id)
                user_id = int(user_id)
                user = client.get_entity(user_id)

                if user:
                    # Удаляем ID сразу после успешного приглашения
                    user_ids.remove(str(user_id))
                    with open(users_file, 'w') as file:
                        file.write('\n'.join(user_ids))
                    client(functions.channels.InviteToChannelRequest(chat_id, [user]))
                    print(f"Пользователь с ID {user_id} приглашен в чат. Удаляю из списка...")

                    sleep(random.randrange(40, 60))
                else:
                    user_ids.remove(str(user_id))
                    with open(users_file, 'w') as file:
                        file.write('\n'.join(user_ids))
                    print(f"Пользователь с ID {user_id} не найден.")
            except PeerFloodError as e:
                print(f"Бан за флуд со стороны Telegram: {e}")
                exit()
            except UserPrivacyRestrictedError:
                print(f"Юзер {user_id} установил настройки 'не приглашать меня в группы'")
            except Exception as e:
                print(e)
                print(f"Ошибка при приглашении пользователя с ID {user_id}: {str(e)}")

    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
