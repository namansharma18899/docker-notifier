from abc import ABC, abstractmethod
from alerts.notify import system_tray_notify

# Notify Interface
class Notify(ABC):
    @abstractmethod
    def send_notification(self, *args, **kwargs):
        pass

class SystemNotification(Notify):
    def send_notification(self, title, message):
        # Simulated System notification logic
        print(f"Sending Slack notification: {message}")
        system_tray_notify(title,message)

# Slack Notification class
class SlackNotification(Notify):
    def send_notification(self, message):
        # Simulated Slack notification logic
        print(f"Sending Slack notification: {message}")

# Email Notification class
class EmailNotification(Notify):
    def send_notification(self, message):
        # Simulated Email notification logic
        print(f"Sending Email notification: {message}")

# Rule Interface
class Rule(ABC):
    @abstractmethod
    def validate(self, data):
        pass

    @abstractmethod
    def get_notification(self):
        pass

# RulesValidator class
class RulesValidator:
    def __init__(self, rules):
        self.rules = rules
        self.notifications = []

    def validate_rules(self, data):
        self.notifications.clear()
        for rule in self.rules:
            if not rule.validate(data):
                notify_action = rule.get_notification()
                if notify_action:
                    notify_action.send_notification(f"Rule '{rule.__class__.__name__}' failed.")
                self.notifications.append(notify_action)
        return len(self.notifications) == 0

    def get_notifications(self):
        return self.notifications

# Example of a concrete rule
class LengthRule(Rule):
    def __init__(self, min_length, notification_type):
        self.min_length = min_length
        self.notification_type = notification_type

    def validate(self, data):
        return len(data) >= self.min_length

    def get_notification(self):
        if self.notification_type:
            return self.notification_type

# Example usage
if __name__ == "__main__":
    slack_notify = SlackNotification()
    email_notify = EmailNotification()

    rules = [
        LengthRule(min_length=5, notification_type=slack_notify),
        LengthRule(min_length=10, notification_type=email_notify)
    ]
    validator = RulesValidator(rules)

    data = "123"
    if not validator.validate_rules(data):
        notifications = validator.get_notifications()
        for notify in notifications:
            if notify:
                notify.send_notification("Additional custom action after notification.")
