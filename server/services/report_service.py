from server.repos.article_repo import ArticleRepository
from server.repos.report_article_repo import ReportManager
from server.config.constants import REPORT_THRESHOLD
from server.services.email_service import EmailService

class ReportService:
    def __init__(self):
        self.article_repo = ArticleRepository()
        self.report_manager = ReportManager()
        self.email_service = EmailService()

    def report_article(self, article_id, user_id, reason):
        self.report_manager.report_article(article_id, user_id, reason)

        report_count = self.report_manager.get_report_count(article_id)
        if report_count >= REPORT_THRESHOLD:
            self.article_repo.hide_article(article_id)

        if report_count < REPORT_THRESHOLD:
            self.email_service.send_notification_email(
                to_email="vickygaur237@gmail.com",
                message=f"Article ID {article_id} was reported by User ID {user_id}.\nReason: {reason or 'No reason provided'}.\nTotal reports: {report_count}"
            )

        return {"message": "Report submitted successfully."}

    def get_reported_articles(self):
        return self.report_manager.get_reported_articles()

    def hide_article(self, article_id):
        return self.article_repo.hide_article(article_id)

    def unhide_article(self, article_id):
        return self.article_repo.unhide_article(article_id)


