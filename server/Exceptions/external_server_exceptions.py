class ExternalServerNotFoundException(Exception):
    def __init__(self, message="server is not found!!!"):
        self.message = message
        super().__init__(self.message)