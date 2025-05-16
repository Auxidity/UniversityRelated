class EmailNotification:
    def send(self, message):
        return f"Sending email: {message}"

class SMSNotification:
    def send(self, message):
        return f"Sending SMS: {message}"

class PushNotification:
    def send(self, message):
        return f"Sending push notification: {message}"

class NotificationManager:
    def __init__(self, notification_type):
        self.notification_type = notification_type
    
    def notify(self, message):
        if self.notification_type == "email":
            notifier = EmailNotification()
        elif self.notification_type == "sms":
            notifier = SMSNotification()
        elif self.notification_type == "push":
            notifier = PushNotification()
        else:
            raise ValueError("Unsupported notification type")
        print(notifier.send(message))

# Example usage
if __name__ == "__main__":
    notification_type = input("Enter notification type (email/sms/push): ").lower()
    message = "This is a test notification."
    
    manager = NotificationManager(notification_type)
    manager.notify(message)

