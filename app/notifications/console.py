from notifications.base import NotificationStrategy

class ConsoleNotification(NotificationStrategy):
    async def notify(self, message: str) -> None:
        print(f"Notification: {message}")
