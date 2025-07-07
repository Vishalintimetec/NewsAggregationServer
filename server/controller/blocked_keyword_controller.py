from server.services.blocked_keyword_service import BlockedKeywordService

class BlockedKeywordController:
    def __init__(self):
        self.service = BlockedKeywordService()

    def block_keyword(self, keyword):
        return self.service.block_keyword(keyword)

    def unblock_keyword(self, keyword):
        return self.service.unblock_keyword(keyword)

    def get_all_keywords(self):
        return self.service.get_all_keywords()