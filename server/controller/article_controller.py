from server.services.report_service import ReportService


class ArticleController:
    def __init__(self):
        self.report_service = ReportService()

    def report_article(self, article_id, user_id, reason):
        return self.report_service.report_article(article_id, user_id, reason)

    def get_reported_articles(self):
        return self.report_service.get_reported_articles()

    def hide_article(self, article_id):
        return self.report_service.hide_article(article_id)

    def unhide_article(self, article_id):
        return self.report_service.unhide_article(article_id)