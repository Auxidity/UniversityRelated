class EmailNotification:
    def send(self, message):
        return f"Sending email: {message}"

class SMSNotification:
    def send(self, message):
        return f"Sending SMS: {message}"

class PushNotification:
    def send(self, message):
        return f"Sending push notification: {message}"


class NotificationFactory:
    _notifications = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification
    }
    
    @staticmethod
    def get_notification_type(notification_type):
        notification = NotificationFactory._notifications.get(notification_type)

        if not notification:
            raise ValueError("Unsupported notification type")
        return notification

class NotificationManager:
    def __init__(self, notification_type):
        self.notification_type = notification_type
        self.notification = NotificationFactory.get_notification_type(notification_type)()

    def notify(self, message):
        print(self.notification.send(message))


# Example usage
if __name__ == "__main__":
    notification_type = input("Enter notification type (email/sms/push): ").lower()
    try:
        message = "This is a test notification."
        
        manager = NotificationManager(notification_type)
        manager.notify(message)
    except ValueError as e:
        print(e)