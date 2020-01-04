import sys, os, time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetAllChatsRequest
from telethon import errors

def initialize(api_id, api_hash):
    try:
        os.mkdir('downloaded_media')
    except:
        pass
    client = TelegramClient('media_downloader', api_id, api_hash)
    client.start()
    return client

def download_media(client, chat_title, skip_until=None):
    chats = client(GetAllChatsRequest(except_ids=[]))
    for _, chat in enumerate(chats.chats):
        if chat.title == chat_title:
            print("found chat with title", chat_title)
            print('attemping to iterate over messages to download media')
            skip_until = skip_until and int(skip_until)
            for message in client.iter_messages(chat, offset_id=skip_until):
                if message.media:
                    while True:
                        print(message.id, message.date, "message has media, downloading")
                        try:
                            client.download_media(message, file='downloaded_media')
                        except errors.FloodWaitError as e:
                            print(message.id, message.date, "failed to download media: flood wait error, were asked to wait for", e.seconds, " but will be waiting for", e.seconds + 120)
                            time.sleep(e.seconds + 120)
                            continue
                        except Exception as e:
                            print(message.id, message.date, "failed to download media")
                            raise e
                        print(message.id, message.date, "media downloaded")
                        break
                else:
                    print(message.id, message.date, "message doesn't have media")
            break

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("Example: python main.py --api-id 12345 --api-hash 1ab1ab1ab1ab1ab --chat-title 'Bunker Reborn' --skip-until 123456")
        print("  --api-id and --api-hash you can generate your at https://my.telegram.org")
        print("  --skip-until is optional, should be a message.id, the code iterates over the messages from the newest to the oldest")
        exit()

    if len(sys.argv) < 7:
        print("Missing arguments, check --help")
        exit(1)

    if not (sys.argv[1] == "--api-id" and sys.argv[2] and sys.argv[3] == "--api-hash" and sys.argv[4]):
        print("Missing arguments --api-id and --api-hash (order can't differ from example in --help)")
        exit(1)

    api_id = sys.argv[2]
    api_hash = sys.argv[4]
    client = initialize(api_id, api_hash)

    if not (sys.argv[5] == "--chat-title" and sys.argv[6]):
        print("Missing argument --chat-title (order can't differ from example in --help)")
        exit(1)
    
    chat_title = sys.argv[6]

    skip_until = None
    if len(sys.argv) == 9 and sys.argv[7] == "--skip-until" and sys.argv[8]:
        skip_until = sys.argv[8]
    
    download_media(client, chat_title, skip_until)