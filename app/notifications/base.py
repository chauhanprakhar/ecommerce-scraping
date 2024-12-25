from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    async def notify(self, message: str) -> None:
        pass
