from server.repos.article_repo import ArticleRepository
from server.repos.personalization_repo import PersonalizationRepo
from server.repos.user_repository import UserRepository
from server.services.blocked_keyword_service import BlockedKeywordService


class UserService:
    def __init__(self):
        self.repo = ArticleRepository()
        self.user_repo = UserRepository()
        self.blocked_keyword_service = BlockedKeywordService()
        self.personalization_repo = PersonalizationRepo()

    def get_user_by_id(self, user_id):
        return self.user_repo.get_user_by_id(user_id)

    def filter_blocked_articles(self, articles):
        blocked_keywords = self.blocked_keyword_service.get_all_keywords()
        filtered = []
        for article in articles:
            title = (article.get('title') or '').lower()
            content = (article.get('content') or '').lower()
            if any(kw.lower() in title or kw.lower() in content for kw in blocked_keywords):
                continue
            filtered.append(article)
        return filtered

    def get_headlines_today(self, user_id):
        articles = self.repo.fetch_headlines_by_day()
        articles = self.filter_blocked_articles(articles)
        return self.personalize_articles(user_id, articles)

    def get_headlines_in_date_range(self, user_id, start, end, category):
        articles = self.repo.fetch_headlines_in_range(start, end, category)
        articles = self.filter_blocked_articles(articles)
        return self.personalize_articles(user_id, articles)

    def get_saved_articles(self, user_id):
        return self.repo.fetch_saved_articles(user_id)

    def save_article(self, user_id, article_id):
        return self.repo.insert_saved_article(user_id, article_id)

    def delete_article(self, user_id, article_id):
        return self.repo.remove_saved_article(user_id, article_id)

    def search_articles(self, user_id, query, start, end, sort_by):
        articles = self.repo.search_articles(query, start, end, sort_by)
        articles = self.filter_blocked_articles(articles)
        return self.personalize_articles(user_id, articles)

    def personalize_articles(self, user_id, articles):
        category_counts = self.personalization_repo.get_user_category_counts(user_id)
        personalized = []
        for article in articles:
            score = 0
            category = article.get('category_name')
            score += category_counts.get(category, 0) * 3
            personalized.append((score, article))
        personalized.sort(reverse=True, key=lambda x: x[0])
        return [a for score, a in personalized[:20]]

    def logout(self, user_id):
        return {"message": f"User {user_id} logged out successfully."}

