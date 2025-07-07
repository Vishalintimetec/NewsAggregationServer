from server.repos.blocked_keyword_repo import BlockedKeywordRepo
from server.Exceptions.blocked_keyword_exceptions import BlockedKeywordNotFoundException

class BlockedKeywordService:
    def __init__(self):
        self.repo = BlockedKeywordRepo()

    def block_keyword(self, keyword):
        result = self.repo.block_keyword(keyword)
        if not result:
            raise BlockedKeywordNotFoundException(f"Failed to block keyword '{keyword}'")
        return result

    def unblock_keyword(self, keyword):
        result = self.repo.unblock_keyword(keyword)
        if not result:
            raise BlockedKeywordNotFoundException(f"Failed to unblock keyword '{keyword}'")
        return result

    def get_all_keywords(self):
        keywords = self.repo.get_all_keywords()
        if not keywords:
            raise BlockedKeywordNotFoundException("No blocked keywords found")
        return keywords