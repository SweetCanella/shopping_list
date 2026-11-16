"""Пользователи системы формирования списка покупок."""


class User:
    """Пользователь, который формирует список покупок."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Сохранить идентификатор, имя и электронную почту."""
        self.id = user_id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        """Преобразовать пользователя в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Создать пользователя из словаря JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def __str__(self) -> str:
        """Вернуть имя пользователя."""
        return self.name
