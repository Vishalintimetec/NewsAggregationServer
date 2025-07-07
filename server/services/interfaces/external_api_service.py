from abc import ABC, abstractmethod


class ExternalAPIService(ABC):

    @abstractmethod
    def fetch_news_articles(self, server_config):
        pass