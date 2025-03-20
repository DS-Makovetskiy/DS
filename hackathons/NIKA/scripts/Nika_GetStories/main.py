from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty
import os
from transliterate import translit

api_id = ''
api_hash = ''
group_username = 'fondnika'
hashtag = '#приветиздома'

# Транслитерация хэштега
transliterated_hashtag = translit(hashtag, reversed=True).replace(' ', '_').replace('#', '')

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Подключение к группе
    await client.start()
    chat = await client.get_entity(group_username)

    # Создание каталога для сообщений, если его нет
    base_folder = 'message_data'
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    # Получение сообщений
    async for message in client.iter_messages(chat, search=hashtag, filter=InputMessagesFilterEmpty):
        message_folder = os.path.join(base_folder, f'{transliterated_hashtag}_{message.id}')
        
        # Если папка уже существует, пропустить скачивание
        if os.path.exists(message_folder):
            print(f'Skipping message {message.id}, folder already exists.')
            continue
        
        # Создание папки для сообщения
        os.makedirs(message_folder)
        
        # Сохранение текста
        if message.text:
            with open(os.path.join(message_folder, 'text.txt'), 'w', encoding='utf-8') as f:
                f.write(message.text)
            print(f'Text saved in {message_folder}/text.txt')
        
        # Сохранение фото
        if message.photo:
            photo_path = os.path.join(message_folder, 'photo.jpg')
            await message.download_media(file=photo_path)
            print(f'Photo saved in {photo_path}')
        
        # Сохранение видео
        if message.video:
            video_path = os.path.join(message_folder, 'video.mp4')
            await message.download_media(file=video_path)
            print(f'Video saved in {video_path}')
        
        # Сохранение ссылки
        if message.web_preview:
            link_path = os.path.join(message_folder, 'link.txt')
            with open(link_path, 'w', encoding='utf-8') as f:
                f.write(message.web_preview.url)
            print(f'Link saved in {link_path}')

with client:
    client.loop.run_until_complete(main())
