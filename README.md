# telegram-media-downloader

A few lines Python 3 script to download all the media from a Telegram chat/group/channel.

## Install the dependencies

```
$ pip install -r requirements.txt
```

## Usage

```
$ python main.py --help
Example: python main.py --api-id 12345 --api-hash 1ab1ab1ab1ab1ab --chat-title 'Bunker Reborn' --skip-until 123456
  --api-id and --api-hash you can generate your at https://my.telegram.org
  --skip-until is optional, should be a message.id, the code iterates over the messages from the newest to the oldest
```