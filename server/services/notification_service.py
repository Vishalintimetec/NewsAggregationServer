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
        # category_id = self.category_repo.get_category_by_name(preference_data.category)["category_id"]
        # print(category_id)
        return self.repo.insert_preference(user_id, preference_data)

    def get_preferences(self, user_id):
        return self.repo.get_preferences_by_user(user_id)

    def configure_notifications(self, user_id, config_data):
        results = []
        for config in config_data.configurations:
            if config.is_enabled:
                for keyword in config.keywords:
                    preference_data = type('obj', (object,), {
                        'category': config.category_name,
                        'keyword': keyword if keyword != 'all' else None
                    })
                    result = self.repo.insert_preference(user_id, preference_data)
                    results.append(result)

        return {"message": f"Notification preferences configured successfully. {len(results)} preferences created."}

    def delete_preference(self, user_id, preference_id):
        return self.repo.delete_preference(user_id, preference_id)


    def generate_notifications_for_new_articles(self):
        self.repo.insert_notifications_for_new_articles()
        print("Notifications inserted based on new articles.")

    def send_unread_notifications(self):
        data = self.repo.get_unread_notifications_grouped_by_user()
        for entry in data:
            self.email_service.send_notification_email(entry['email'], entry['messages'])