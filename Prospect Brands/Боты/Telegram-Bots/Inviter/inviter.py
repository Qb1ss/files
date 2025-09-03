# основной: 25685716 | 4d41cb933dcb53557601065985e373a3
# рабочий "Агентство 404": 28410150 | ee1a49641055557a1b6dd210849ade6d

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.sync import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep
import random

#############################################
# --- НЕОБХОДИМО ЗАПОЛНИТЬ!!! ---
#
api_id = 28410150
api_hash = 'ee1a49641055557a1b6dd210849ade6d'
# -Название чата или канала, куда приглашать юзеров (без @)
chat_name = 'prspctmarket' # welcome_prospect_1 #'prspctmarket'

# Не трогать
# -Название файла, в котором хранятся userId (должен находится в одной директории со скриптом)
users_file = 'user_parsered_Kicksy.txt'
device_model = "Pixel 3 XL"
system_version = "Android 10.0"

max_value_invating = 5

##########################################

def starting():
    print("Настройки инвайтера")

    invating()

def invating():
    print("Start invating...")
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
                    user = client.get_dialocs(user_id)

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
                    print(f"\nОшибка при приглашении пользователя с ID {user_id}: {str(e)}")

        except Exception as e:
            print(f"Ошибка при чтении файла: {str(e)}")


if __name__ == '__main__':
    starting()