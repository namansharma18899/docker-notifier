from plyer import notification

def system_tray_notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Process Monitor",
        timeout=10  # Notification will stay for 10 seconds
    )
