from server.repos.external_server_repo import ExternalServerRepository
class APIManager:
    def __init__(self):
        self.external_server_repo = ExternalServerRepository()

    def get_active_api(self):
        apis = self.external_server_repo.get_all_servers()
        return next((api for api in apis if api["is_active"] == 1), None)

    def get_all_server_details(self):
        return self.external_server_repo.get_all_servers()