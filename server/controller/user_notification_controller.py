from server.services.notification_service import NotificationService

class NotificationController:
    def __init__(self):
        self.service = NotificationService()

    def create_preference(self, user_id, preference_data):
        return self.service.create_preference(user_id, preference_data)

    def get_preferences(self, user_id):
        return self.service.get_preferences(user_id)

    # def update_preference(self, user_id, preference_id, preference_data):
    #     return self.service.update_preference(user_id, preference_id, preference_data)

    # controller/user_controller.py
    def configure_notifications(self, user_id, config_data):
        return self.service.configure_notifications(user_id, config_data)

    def delete_preference(self, user_id, preference_id):
        return self.service.delete_preference(user_id, preference_id)

    def get_unread_notifications(self, user_id):
        return self.service.get_unread_notifications(user_id)
