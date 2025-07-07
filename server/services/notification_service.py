from server.repos.category_repo import CategoryRepo
from server.repos.notification_repo import NotificationRepo
from server.services.email_service import EmailService


class NotificationService:
    def __init__(self):
        self.repo = NotificationRepo()
        self.category_repo = CategoryRepo()
        self.email_service = EmailService()

    def create_preference(self, user_id, preference_data):
        print(preference_data.category)
        return self.repo.insert_preference(user_id, preference_data)

    def get_preferences(self, user_id):
        return self.repo.get_preferences_by_user(user_id)

    def configure_notifications(self, user_id, config_data):
        return self.repo.configure_notifications(user_id, [c.dict() for c in config_data.configurations])

    def get_unread_notifications(self, user_id):
        unread_articles =  self.repo.get_unread_notifications(user_id)
        self.repo.mark_notification_as_read(user_id)
        return unread_articles

    def delete_preference(self, user_id, preference_id):
        return self.repo.delete_preference(user_id, preference_id)


    def generate_notifications_for_new_articles(self):
        self.repo.insert_notifications_for_new_articles()
        print("Notifications inserted based on new articles.")

    def send_unread_notifications(self):
        data = self.repo.get_unread_notifications_grouped_by_user()
        for entry in data:
            self.email_service.send_notification_email(entry['email'], entry['messages'])