import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id = channel['items'][0]['id']
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subscriber_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return youtube

    def to_json(self, filename):
        """
        Coхраняет в файл значения атрибутов экземпляра `Channel`
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, 'w', encoding="windows-1251") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count == other.subscriber_count
