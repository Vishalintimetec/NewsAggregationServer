from server.repos.external_server_repo import ExternalServerRepository
from server.schemas.external_servers import ExternalServerUpdate
from server.Exceptions.external_server_exceptions import ExternalServerNotFoundException
from typing import List

class ExternalServerService:
    def __init__(self):
        self.repo = ExternalServerRepository()

    def get_all_servers(self) -> List[dict]:
        return self.repo.get_all_servers()

    def update_server_details(self, server_id: int, server: ExternalServerUpdate) -> dict:
        existing_server = self.repo.get_server_by_id(server_id)
        if not existing_server:
            raise ExternalServerNotFoundException(f"Server with ID {server_id} not found")
        return self.repo.update_server_details(server_id, server)
