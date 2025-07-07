from server.services.newsapi_service import NewsAPIService
from server.services.thenewsapi_service import TheNewsAPIService
from server.services.interfaces.external_api_service import ExternalAPIService

class ExternalAPIServiceFactory:
    @staticmethod
    def get_service(server_name: str) -> ExternalAPIService:
        if 'thenewsapi' in server_name.lower():
            return TheNewsAPIService()
        else:
            return NewsAPIService()