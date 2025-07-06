from server.repos.blocked_keyword_repo import BlockedKeywordRepo

class BlockedKeywordService:
    def __init__(self):
        self.repo = BlockedKeywordRepo()

    def block_keyword(self, keyword):
        return self.repo.block_keyword(keyword)

    def unblock_keyword(self, keyword):
        return self.repo.unblock_keyword(keyword)

    def get_all_keywords(self):
        return self.repo.get_all_keywords()